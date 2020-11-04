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

VERSION = '4.1 4-Nov-2020'

BAR_WIDTH = 20
BAR_SPACING = 30
EDGE_OFFSET = 3
GRAPH_SIZE = (300,150)
DATA_SIZE = (500,300)
MAX_ROWS, MAX_COLS = 2, 4
DEFAULT_GROWTH_RATE = 1.25      # default for forecasting
DISPLAY_DAYS = 30               # default number of days to display
MAX_FORECASTED_DAYS = 100

# LINK_CONFIRMED_DATA = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
LINK_CONFIRMED_DATA = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

# LINK_DEATHS_DATA = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
LINK_DEATHS_DATA = r"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"


sg.theme('Dark Blue 17')


DEFAULT_SETTINGS = {'rows':MAX_ROWS, 'cols':MAX_COLS, 'theme':'Dark Blue 17', 'forecasting':False,
                    'graph_x_size':GRAPH_SIZE[0], 'graph_y_size':GRAPH_SIZE[1], 'display days':DISPLAY_DAYS,
                    'data source':'confirmed', 'cumulative':True}
DEFAULT_LOCATIONS = ['Worldwide', 'US', 'China', 'Italy', 'Iran',  'France', 'Spain',  'United Kingdom', ]

SETTINGS_FILE = path.join(path.dirname(__file__), r'C19-Graph.cfg')

settings = {}

ICON = b'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'
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
    with open(SETTINGS_FILE, 'w+') as f:
        jsondump(settings, f)


def change_settings(settings):
    global SETTINGS_FILE

    data_is_deaths = settings.get('data source', 'confirmed') == 'deaths'
    layout = [
              [sg.T('Display'),
               sg.Radio('Deaths', 1, default=data_is_deaths, key='-DATA DEATHS-'),
               sg.Radio('Confirmed Cases', 1, default=not data_is_deaths, key='-DATA CONFIRMED-'), ],
              [sg.Checkbox('Cumulative', default=settings.get('cumulative', DEFAULT_SETTINGS['cumulative']), key='-CUMULATIVE-')],
              [sg.T('Color Theme')],
              [sg.Combo(sg.theme_list(), default_value=settings.get('theme', DEFAULT_SETTINGS['theme']), size=(20,20), key='-THEME-' )],
              [sg.T('Display Rows', size=(15,1), justification='r'), sg.In(settings.get('rows',''), size=(4,1), key='-ROWS-' )],
              [sg.T('Display Cols', size=(15,1), justification='r'), sg.In(settings.get('cols',''), size=(4,1), key='-COLS-' )],
              [sg.T('Graph size in pixels'), sg.In(settings.get('graph_x_size',''), size=(4,1), key='-GRAPHX-'), sg.T('X'), sg.In(settings.get('graph_y_size',''), size=(4,1), key='-GRAPHY-')],
              [sg.CBox('Autoscale Graphs', default=settings.get('autoscale',True), key='-AUTOSCALE-'),
               sg.T('Max Graph Value'),
               sg.In(settings.get('graphmax',''), size=(6,1), key='-GRAPH MAX-')],
              [sg.T('Number of days to display (0 for all)'), sg.In(settings.get('display days',''), size=(4,1), key='-DISPLAY DAYS-')],
              [sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)],]

    window = sg.Window('Settings', layout, icon=ICON, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()

    if event == 'Ok':
        settings['theme'] = values['-THEME-']
        settings['rows'] = int(values['-ROWS-'])
        settings['cols'] = int(values['-COLS-'])
        settings['autoscale'] = values['-AUTOSCALE-']
        settings['graphmax'] = values['-GRAPH MAX-']
        settings['cumulative'] = values['-CUMULATIVE-']
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
    max_col = 7
    row = []
    cb_layout = []
    for i, location in enumerate(sorted(locations)):
        row.append(sg.CB(location, size=(15,1), pad=(1,1), font='Any 9', key=location, default=True if location in defaults else False))
        if (i+1) % max_col == 0:
            cb_layout += [row]
            row = []
    cb_layout += [row]

    layout = [[sg.T('Choose Locations')]]
    layout += cb_layout
    layout += [[sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)]]

    window = sg.Window('Choose Locations', layout, icon=ICON, keep_on_top=True, border_depth=0)
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
    arrow = '↑' if up > 0 else '↓'
    if future_days:
        window[f'-TITLE-{graph_num}'].update(f'{location} EST in {future_days} days\n{int(max(values)):8,} {arrow} {int(up):,} Δ {delta:3.0f}%')
    else:
        window[f'-TITLE-{graph_num}'].update(f'{location} {int(max(values)):8,} {arrow} {int(up):,} Δ {delta:3.0f}%')
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

def prepare_data(link, settings):
    """
    Downloads the CSV file and creates a dictionary containing the data
    Dictionary:      Location (str,str) : Data [ int, int, int, ...  ]
    :return:        Dict[(str,str):List[int]]
    """

    data = download_data(link)
    # remove blank rows
    new_data = []
    for row in data:
        if row:
            new_data.append(row)
    data = new_data

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

        if settings.get('cumulative', True):
            loc_data_dict[(loc_country, 'Total')] = totals
        else:
            deltas = []
            for i, x in enumerate(totals):
                deltas.append(x - totals[i-1] if i != 0 else 0)
            loc_data_dict[(loc_country, 'Total')] = deltas


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
            graph_row += [sg.Frame('', [[sg.T(size=(30,2), key=f'-TITLE-{row*max_cols+col}', font='helvetica 9')],[graph]], pad=(0,0))]
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
                sg.T(f'Rewind up to 00000 days', key='-REWIND MESSAGE-'),
                sg.CB('Animate Graphs', enable_events=True, key='-ANIMATE-'), sg.T('Update every'), sg.I('50', key='-ANIMATION SPEED-', enable_events=True, size=(4,1)), sg.T('milliseconds')],
               [sg.CB('Enable Forecasting', default=settings.get('forecasting',False), enable_events=True, key='-FORECAST-'), sg.T('       Daily growth rate'), sg.I(str(DEFAULT_GROWTH_RATE), size=(5,1), key='-GROWTH RATE-'),
                sg.T(f'Forecast up to {MAX_FORECASTED_DAYS} days'),
                sg.Slider((0, MAX_FORECASTED_DAYS), default_value=1, size=(30, 15), orientation='h', enable_events=True, key='-FUTURE SLIDER-'),
                ]]
    layout += [[sg.T('Settings', key='-SETTINGS-', enable_events=True),
                 sg.T('     Locations', key='-LOCATIONS-', enable_events=True),
                 sg.T('     Refresh', key='-REFRESH-', enable_events=True),
                 sg.T('     Change Settings File', key='-CHANGE SETTINGS FILENAME-', enable_events=True),
                 # sg.T('     Raw Data', key='-RAW DATA-', enable_events=True),
                 sg.T('     Exit', key='Exit', enable_events=True),
                 sg.T(' '*20),
                 sg.T(size=(40,2), font='Any 8', key='-UPDATED-'),
                 sg.Col([[sg.T(r'Data source: Johns Hopkins - https://github.com/CSSEGISandData/COVID-19', enable_events=True, font='Any 8', key='-SOURCE LINK-', pad=(0,0))],
                [sg.T(f'Version {VERSION} Created using PySimpleGUI', font='Any 8', enable_events=True, key='-PSG LINK-', pad=(0,0))]])]
                ]

    window = sg.Window('COVID-19 Confirmed Cases', layout, grab_anywhere=False, no_titlebar=False, margins=(0,0), icon=ICON,  finalize=True)

    # set cursor to hand for all text elements that looks like links
    _ = [window[key].set_cursor('hand2') for key in ('-SETTINGS-', '-LOCATIONS-', '-REFRESH-', 'Exit', '-SOURCE LINK-', '-PSG LINK-')]

    return window

def main(refresh_minutes):
    global SETTINGS_FILE

    refresh_time_milliseconds = refresh_minutes*60*1000

    settings = load_settings()
    sg.theme(settings['theme'])
    data_link = LINK_CONFIRMED_DATA if settings.get('data source','confirmed') == 'confirmed' else LINK_DEATHS_DATA
    loc_data_dict = prepare_data(data_link, settings)
    num_data_points = len(loc_data_dict[("Worldwide", "Total")])
    keys = loc_data_dict.keys()
    countries = set([k[0] for k in keys])
    chosen_locations = settings.get('locations',[])
    if not chosen_locations:
        chosen_locations = choose_locations(countries, [])
        save_settings(settings, chosen_locations)

    window = create_window(settings)

    window['-SLIDER-'].update(range=(0,num_data_points-1))
    window['-REWIND MESSAGE-'].update(f'Rewind up to {num_data_points-1} days')

    update_window(window, loc_data_dict, chosen_locations, settings, 0, 1, DEFAULT_GROWTH_RATE)

    animating, animation_refresh_time = False, 1.0

    while True:         # Event Loop
        timeout = animation_refresh_time if animating else refresh_time_milliseconds
        event, values = window.read(timeout=timeout)
        if event in (None, 'Exit', '-QUIT-'):
            break

        if event == '-CHANGE SETTINGS FILENAME-':
            new_filename = sg.popup_get_file('New settings file to use', 'New Settings Filename', default_path=SETTINGS_FILE, initial_folder=path.dirname(SETTINGS_FILE), file_types=(("Settings Files","*.cfg"),))
            if new_filename and path.exists(new_filename):
                SETTINGS_FILE = new_filename
                settings = load_settings()
                chosen_locations = settings.get('locations', [])
                event = '-SETTINGS-'        # fake a user clicking "change settings"
            elif new_filename:              # if didn't exist, then save current settings to new file
                SETTINGS_FILE = new_filename
                save_settings(settings, chosen_locations)
        if event == '-SETTINGS-':           # "Settings" at bottom of window
            settings = change_settings(settings)
            save_settings(settings, chosen_locations)
            sg.theme(settings['theme'] if settings.get('theme') else sg.theme())
            data_link = LINK_CONFIRMED_DATA if settings.get('data source', 'confirmed') == 'confirmed' else LINK_DEATHS_DATA
            loc_data_dict = prepare_data(data_link, settings)
            window.close()
            window = create_window(settings)
            window['-SLIDER-'].update(range=(0, num_data_points-1))
            window['-REWIND MESSAGE-'].update(f'Rewind up to {num_data_points-1} days')
        elif event == '-LOCATIONS-':        # "Location" text at bottom of window
            chosen_locations = choose_locations(countries, chosen_locations)
            save_settings(settings, chosen_locations)
        elif event == '-FORECAST-':         # Changed Forecast checkbox
            settings['rows'] = settings['rows']*2 if values['-FORECAST-'] else settings['rows']//2
            settings['forecasting'] = values['-FORECAST-']
            save_settings(settings, chosen_locations)
            window.close()
            window = create_window(settings)
            window['-SLIDER-'].update(range=(0, num_data_points - 1))
            window['-REWIND MESSAGE-'].update(f'Rewind up to {num_data_points - 1} days')
        elif event == '-SOURCE LINK-':      # Clicked on data text, open browser
            webopen(r'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series')
        elif event == '-PSG LINK-':      # Clicked on data text, open browser
            webopen(r'http://www.PySimpleGUI.com')
        elif event == '-RAW DATA-':
            sg.Print(loc_data_dict[("Worldwide","Total")])
        elif event == '-ANIMATE-':
            animating = values['-ANIMATE-']
            animation_refresh_time = int(values['-ANIMATION SPEED-'])

        if animating:
            new_slider = values['-SLIDER-']-1 if values['-SLIDER-'] else num_data_points
            window['-SLIDER-'].update(new_slider)

        if event in (sg.TIMEOUT_KEY, '-REFRESH-') and not animating:
            sg.popup_quick_message('Updating data', font='Any 20')
            loc_data_dict = prepare_data(data_link, settings)
            num_data_points = len(loc_data_dict[("Worldwide", "Total")])

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
