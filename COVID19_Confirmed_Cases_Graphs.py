import PySimpleGUI as sg
from urllib import request
from csv import reader as csvreader
from json import load as jsonload
from json import dump as jsondump
from os import path
from datetime import datetime
from webbrowser import open as webopen


"""
    Graph COVID-19 Confirmed Cases
    
    A Tableau-style grid of graphs so that one country can be easily compared to another.
    
    The "settings" window has not been completed yet so things like choosing which countries and whether or not
    to show details are things yet to be done, but SOON!  
    
    A work in progress... evolving by the hour...
    
    Use the Johns Hopkins datasets to graphical display and analyse the spread of the C19 virus over time.
    The data is housed on the Johns Hopkins Covid19 GitHub Repository:
        https://github.com/CSSEGISandData/COVID-19
    
    
    Copyright 2020 PySimpleGUI.com

"""

BAR_WIDTH = 20
BAR_SPACING = 30
NUM_BARS = 20
EDGE_OFFSET = 3
GRAPH_SIZE = (300,150)
DATA_SIZE = (500,300)
MAX_ROWS = 2
MAX_COLS = 4
DEFAULT_GROWTH_RATE = 1.25      # default for forecasting
DISPLAY_DAYS = 30               # default number of days to display
MAX_FORECASTED_DAYS = 100

LINK_CONFIRMED_DATA = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'

LINK_DEATHS_DATA = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"



sg.theme('Dark Blue 17')


DEFAULT_SETTINGS = {'rows':MAX_ROWS, 'cols':MAX_COLS, 'theme':'Dark Blue 17', 'forecasting':False,
                    'graph_x_size':GRAPH_SIZE[0], 'graph_y_size':GRAPH_SIZE[1], 'display days':DISPLAY_DAYS,
                    'data source':'confirmed'}
DEFAULT_LOCATIONS = ['Worldwide', 'US', 'China', 'Italy', 'Iran',  'France', 'Spain',  'United Kingdom', ]

SETTINGS_FILE = path.join(path.dirname(__file__), r'C19-Graph.cfg')

settings = {}


########################################## SETTINGS ##########################################
def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = jsonload(f)
    except:
        sg.popup_quick_message('No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = change_settings(DEFAULT_SETTINGS)
        save_settings(settings)
    return settings


def save_settings(settings, chosen_locations=None):
    if chosen_locations:
        settings['locations'] = chosen_locations
    with open(SETTINGS_FILE, 'w') as f:
        jsondump(settings, f)


def change_settings(settings):
    data_is_deaths = settings.get('data source', 'confirmed') == 'deaths'
    layout = [[sg.T('Color Theme')],
              [sg.T('Display'), sg.Radio('Deaths', 1, default=data_is_deaths, key='-DATA DEATHS-'), sg.Radio('Confirmed Cases', 1, default=not data_is_deaths, key='-DATA CONFIRMED-')],
              [sg.Combo(sg.theme_list(), default_value=settings.get('theme', DEFAULT_SETTINGS['theme']), size=(20,20), key='-THEME-' )],
              [sg.T('Display Rows', size=(15,1), justification='r'), sg.In(settings.get('rows',''), size=(4,1), key='-ROWS-' )],
              [sg.T('Display Cols', size=(15,1), justification='r'), sg.In(settings.get('cols',''), size=(4,1), key='-COLS-' )],
              [sg.T('Graph size in pixels'), sg.In(settings.get('graph_x_size',''), size=(4,1), key='-GRAPHX-'), sg.T('X'), sg.In(settings.get('graph_y_size',''), size=(4,1), key='-GRAPHY-')],
              [sg.CBox('Autoscale Graphs', default=settings.get('autoscale',True), key='-AUTOSCALE-'),
               sg.T('Max Graph Value'),
               sg.In(settings.get('graphmax',''), size=(6,1), key='-GRAPH MAX-')],
              [sg.T('Number of days to display (0 for all)'), sg.In(settings.get('display days',''), size=(4,1), key='-DISPLAY DAYS-')],
              [sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)],]

    window = sg.Window('Settings', layout, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()

    if event == 'Ok':
        settings['theme'] = values['-THEME-']
        settings['rows'] = int(values['-ROWS-'])
        settings['cols'] = int(values['-COLS-'])
        settings['autoscale'] = values['-AUTOSCALE-']
        settings['graphmax'] = values['-GRAPH MAX-']
        try:
            settings['graph_x_size'] = int(values['-GRAPHX-'])
            settings['graph_y_size'] = int(values['-GRAPHY-'])
        except:
            settings['graph_x_size'] = GRAPH_SIZE[0]
            settings['graph_y_size'] = GRAPH_SIZE[1]
        try:
            settings['display days'] = int(values['-DISPLAY DAYS-'])
        except:
            settings['display days'] = 0
        settings['data source'] = 'deaths' if values['-DATA DEATHS-'] else 'confirmed'

    return settings


def choose_locations(locations, chosen_locations):
    locations = list(locations)
    if not chosen_locations:
        defaults = DEFAULT_LOCATIONS
    else:
        defaults = chosen_locations
    max_col = 6
    row = []
    cb_layout = []
    for i, location in enumerate(sorted(locations)):
        row.append(sg.CB(location, size=(15,1), key=location, default=True if location in defaults else False))
        if (i+1) % max_col == 0:
            cb_layout += [row]
            row = []
    cb_layout += [row]

    layout = [[sg.T('Choose Locations')]]
    layout += cb_layout
    layout += [[sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)]]

    window = sg.Window('Choose Locations', layout, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()

    if event == 'Ok':
        locations_selected = []
        for key in values.keys():
            if values[key]:
                locations_selected.append(key)
    else:
        locations_selected = chosen_locations

    return locations_selected



########################################## DOWNLOAD DATA ##########################################

def download_data(link):

    # Download and parse the CSV file
    file_url = link
    data = [d.decode('utf-8') for d in request.urlopen(file_url).readlines()]

    # Add blank space for missing cities to prevent dropping columns
    for n, row in enumerate(data):
        data[n] = " " + row if row[0] == "," else row

    # Split each row into a list of data
    data_split = [row for row in csvreader(data)]

    return data_split

########################################## UPDATE WINDOW ##########################################

def estimate_future(data, num_additional, rate):
    new_data = [x for x in data]
    for i in range(num_additional):
        # new_data.append(new_data[-1]*rate)
        new_data.append(new_data[-1] + ((new_data[-1]-new_data[-2]) * rate))
    return new_data


def draw_graph(window, location, graph_num, values, settings, future_days):
    # update title
    try:
        delta = (values[-1]-values[-2])/values[-2]*100
        up = values[-1]-values[-2]
    except:
        delta = up = 0

    start = len(values)-settings['display days']
    if start < 0 or settings['display days'] == 0:
        start = 0
    values = values[start:]
    if future_days:
        window[f'-TITLE-{graph_num}'].update(f'{location} EST in {future_days} days\n{int(max(values)):8,} ↑ {int(up):,} Δ {delta:3.0f}%')
    else:
        window[f'-TITLE-{graph_num}'].update(f'{location} {int(max(values)):8,} ↑ {int(up):,} Δ {delta:3.0f}%')
    graph = window[graph_num]
    # auto-scale the graph.  Will make this an option in the future
    if settings.get('autoscale', True):
        max_value = max(values)
    else:
        try:
            max_value = int(settings.get('graphmax', max(values)))
        except:
            max_value = max(values)
    graph.change_coordinates((0, 0), (DATA_SIZE[0], max_value))
    # calculate how big the bars should be
    num_values = len(values)
    bar_width_total = DATA_SIZE[0] / num_values
    bar_width = bar_width_total * 2 / 3
    bar_width_spacing = bar_width_total
    # Draw the Graph
    graph.erase()
    for i, graph_value in enumerate(values):
        bar_color = sg.theme_text_color()  if i < num_values-future_days else 'red'
        if graph_value:
            graph.draw_rectangle(top_left=(i * bar_width_spacing + EDGE_OFFSET, graph_value),
                                 bottom_right=(i * bar_width_spacing + EDGE_OFFSET + bar_width, 0),
                                 line_width=0,
                                 fill_color=bar_color)


def update_window(window, loc_data_dict, chosen_locations, settings, subtract_days, future_days, growth_rate):
    max_rows, max_cols = int(settings['rows']), int(settings['cols'])
    # Erase all the graphs
    for row in range(max_rows):
        for col in range(max_cols):
            window[row*max_cols+col].erase()
            window[f'-TITLE-{row*max_cols+col}'].update('')
    # Display date of last data point
    header = loc_data_dict[('Header','')]
    end_date = header[-(subtract_days+1)]
    start = len(header)-settings['display days']-(subtract_days+1)
    if start < 0 or settings['display days'] == 0:
        start = 0
    start_date = header[start]
    window['-DATE-'].update(f'{start_date} - {end_date}')
    # Draw the graphs
    for i, loc in enumerate(chosen_locations):
        if i >= max_cols * max_rows:
            break
        values = loc_data_dict[(loc, 'Total')]
        if subtract_days:
            values = values[:-subtract_days]

        draw_graph(window, loc, i, values, settings, 0)

    starting_graph = i+1

    if future_days:
        for i, loc in enumerate(chosen_locations):
            graph_num = starting_graph + i
            if graph_num >= max_cols * max_rows:
                break
            values = loc_data_dict[(loc, 'Total')]
            new_values = estimate_future(values, future_days, growth_rate)

            draw_graph(window, loc, graph_num, new_values, settings, future_days)


    window['-UPDATED-'].update('Updated ' + datetime.now().strftime("%B %d %I:%M:%S %p") + f'\nDate of last datapoint {loc_data_dict[("Header","")][-1]}')

########################################## MAIN ##########################################


##############################################################
# Data Format of CSV File                                    #
#   0                   1       2         3       4      5   #
# State/Province    Country     Lat     Long    1/22    1/23 #
##############################################################

def prepare_data(link):
    """
    Downloads the CSV file and creates a dictionary containing the data
    Dictionary:      Location (str,str) : Data [ int, int, int, ...  ]
    :return:        Dict[(str,str):List[int]]
    """

    data = download_data(link)
    header = data[0][4:]
    graph_data = [row[4:] for row in data[1:]]
    graph_values = []
    for row in graph_data:
        graph_values.append([int(d) if d!= '' else 0 for d in row])
    # make list of countries as tuples (country, privince/state)
    locations = list(set([(row[1], row[0]) for row in data[1:]]))
    locations.append(('Worldwide', ''))
    # Make single row of data per country that will be graphed
    # Location - Data dict.  For each location contains the totals for that location
    # { tuple : list }
    loc_data_dict = {}
    data_points = len(graph_data[0])
    for loc in locations:
        loc_country = loc[0]
        totals = [0]*data_points
        for i, row in enumerate(data[1:]):
            if loc_country == row[1] or loc_country == 'Worldwide':
                loc_data_dict[(loc_country, row[0])] = row[4:]
                for j, d in enumerate(row[4:]):
                    totals[j] += int(d if d!= '' else 0)
        loc_data_dict[(loc_country, 'Total')] = totals

    loc_data_dict[('Header','')] = header

    return loc_data_dict


def create_window(settings):
    max_rows, max_cols = int(settings['rows']), int(settings['cols'])
    graph_size = int(settings['graph_x_size']), int(settings['graph_y_size'])
    # Create grid of Graphs with titles
    graph_layout = [[]]
    for row in range(max_rows):
        graph_row = []
        for col in range(max_cols):
            graph = sg.Graph(graph_size, (0,0), DATA_SIZE, key=row*max_cols+col, pad=(0,0))
            graph_row += [sg.Column([[sg.T(size=(30,2), key=f'-TITLE-{row*max_cols+col}')],[graph]], pad=(0,0))]
        graph_layout += [graph_row]

    if settings.get('data source','confirmed') == 'confirmed':
        heading = 'COVID-19 Cases By Region      '
    else:
        heading = 'COVID-19 Deaths By Region      '

    # Create the layout
    layout = [[sg.T(heading, font='Any 20'),
               sg.T(size=(15,1), font='Any 20', key='-DATE-')],]
    layout += graph_layout
    layout += [[sg.T('Way-back machine'),
                sg.Slider((0,100), size=(30,15), orientation='h', enable_events=True, key='-SLIDER-'),
                sg.T(f'Rewind up to 00000 days', key='-REWIND MESSAGE-')],
               [sg.CB('Enable Forecasting', default=settings.get('forecasting',False), enable_events=True, key='-FORECAST-'), sg.T('       Daily growth rate'), sg.I(str(DEFAULT_GROWTH_RATE), size=(5,1), key='-GROWTH RATE-'),
                sg.T(f'Forecast up to {MAX_FORECASTED_DAYS} days'),
                sg.Slider((0, MAX_FORECASTED_DAYS), default_value=1, size=(30, 15), orientation='h', enable_events=True, key='-FUTURE SLIDER-'),
                ]]
    layout += [[sg.T('Settings', key='-SETTINGS-', enable_events=True),
                 sg.T('     Locations', key='-LOCATIONS-', enable_events=True),
                 sg.T('     Refresh', key='-REFRESH-', enable_events=True),
                 sg.T('     Exit', key='Exit', enable_events=True),
                 sg.T(' '*20),
                 sg.T(size=(40,2), font='Any 8', key='-UPDATED-'),
                 sg.T(r'Data source: Johns Hopkins - https://github.com/CSSEGISandData/COVID-19'+'\nCreated using PySimpleGUI', size=(None, 2), enable_events=True, font='Any 8', key='-SOURCE LINK-'),
                ]]

    window = sg.Window('COVID-19 Confirmed Cases', layout, grab_anywhere=False, no_titlebar=False, margins=(0,0),  finalize=True)

    [window[key].set_cursor('hand2') for key in ['-SETTINGS-', '-LOCATIONS-', '-REFRESH-', 'Exit', '-SOURCE LINK-']]

    return window

def main(refresh_minutes):
    settings = load_settings()
    sg.theme(settings['theme'])
    data_link = LINK_CONFIRMED_DATA if settings.get('data source','confirmed') == 'confirmed' else LINK_DEATHS_DATA
    loc_data_dict = prepare_data(data_link)
    keys = loc_data_dict.keys()
    countries = set([k[0] for k in keys])
    chosen_locations = settings.get('locations',[])
    if not chosen_locations:
        chosen_locations = choose_locations(countries, [])
        save_settings(settings, chosen_locations)

    window = create_window(settings)

    window['-SLIDER-'].update(range=(0,len(loc_data_dict[("Worldwide","Total")])-1))
    window['-REWIND MESSAGE-'].update(f'Rewind up to {len(loc_data_dict[("Worldwide","Total")])-1} days')

    update_window(window, loc_data_dict, chosen_locations, settings, 0, 1, DEFAULT_GROWTH_RATE)

    while True:         # Event Loop
        event, values = window.read(timeout=refresh_minutes*60*1000)
        if event in (None, 'Exit', '-QUIT-'):
            break
        if event == '-SETTINGS-':           # "Settings" at bottom of window
            settings = change_settings(settings)
            save_settings(settings, chosen_locations)
            sg.theme(settings['theme'] if settings.get('theme') else sg.theme())
            new_data_link = LINK_CONFIRMED_DATA if settings.get('data source', 'confirmed') == 'confirmed' else LINK_DEATHS_DATA
            if new_data_link != data_link:
                data_link = new_data_link
                loc_data_dict = prepare_data(data_link)
            window.close()
            window = create_window(settings)
            window['-SLIDER-'].update(range=(0, len(loc_data_dict[("Worldwide", "Total")]) - 1))
            window['-REWIND MESSAGE-'].update(f'Rewind up to {len(loc_data_dict[("Worldwide", "Total")]) - 1} days')
        elif event == '-LOCATIONS-':        # "Location" text at bottom of window
            chosen_locations = choose_locations(countries, chosen_locations)
            save_settings(settings, chosen_locations)
        elif event == '-FORECAST-':         # Changed Forecast checkbox
            settings['rows'] = settings['rows']*2 if values['-FORECAST-'] else settings['rows']//2
            settings['forecasting'] = values['-FORECAST-']
            save_settings(settings, chosen_locations)
            window.close()
            window = create_window(settings)
            window['-SLIDER-'].update(range=(0, len(loc_data_dict[("Worldwide", "Total")]) - 1))
            window['-REWIND MESSAGE-'].update(f'Rewind up to {len(loc_data_dict[("Worldwide", "Total")]) - 1} days')
        elif event == '-SOURCE LINK-':      # Clicked on data text, open browser
            webopen(r'https://github.com/CSSEGISandData/COVID-19')

        if event in (sg.TIMEOUT_KEY, '-REFRESH-'):
            sg.popup_quick_message('Updating data', font='Any 20')
            loc_data_dict = prepare_data(data_link)

        if values['-FORECAST-']:
            try:
                growth_rate = float(values['-GROWTH RATE-'])
            except:
                growth_rate = 1.0
                window['-GROWTH RATE-'](1.0)
            future_days = int(values['-FUTURE SLIDER-'])
        else:
            growth_rate = future_days = 0

        update_window(window, loc_data_dict, chosen_locations, settings, int(values['-SLIDER-']), future_days, growth_rate)

    window.close()


if __name__ == '__main__':
    main(refresh_minutes=20)
