import PySimpleGUI as sg
from urllib import request
from csv import reader as csvreader
from json import load as jsonload
from json import dump as jsondump
from os import path
from datetime import datetime

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
MAX_ROWS = 4
MAX_COLS = 4

sg.theme('Dark Purple 6')

DEFAULT_SETTINGS = {'rows':MAX_ROWS, 'cols':MAX_COLS, 'theme':'Dark Purple 6'}

SETTINGS_FILE = path.join(path.dirname(__file__), r'C19-Graph.cfg')

settings = {}

date_of_final_datapoint = ''

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


def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        jsondump(settings, f)


def change_settings(settings):
    layout = [[sg.T('Color Theme')],
              [sg.Combo(sg.theme_list(), default_value=settings.get('theme', DEFAULT_SETTINGS['theme']), size=(20,20), key='-THEME-' )],
              [sg.T('Display Rows', size=(15,1), justification='r'), sg.In(settings.get('rows',''), size=(4,1), key='-ROWS-' )],
              [sg.T('Display Cols', size=(15,1), justification='r'), sg.In(settings.get('cols',''), size=(4,1), key='-COLS-' )],
              [sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)],]

    window = sg.Window('Settings', layout, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()

    if event == 'Ok':
        settings['theme'] = values['-THEME-']
        settings['rows'] = values['-ROWS-']
        settings['cols'] = values['-COLS-']
        save_settings(settings)

    return settings

def choose_locations(locations):
    locations = list(locations)
    # locations.append('Worldwide')
    # print(locations)
    defaults = ['Worldwide', 'US', 'China', 'Italy', 'Iran', 'Korea, South', 'France', 'Spain', 'Germany', 'United Kingdom', 'Japan', 'Norway', 'Switzerland', 'Australia', 'Canada', 'Netherlands', ]
    max_col = 4
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

    locations_selected = []
    for key in values.keys():
        if values[key]:
            locations_selected.append(key)
    return locations_selected



########################################## DOWNLOAD DATA ##########################################

def download_data():

    # Download and parse the CSV file
    file_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    data = [d.decode('utf-8') for d in request.urlopen(file_url).readlines()]

    # Add blank space for missing cities to prevent dropping columns
    for n, row in enumerate(data):
        data[n] = " " + row if row[0] == "," else row

    # Split each row into a list of data
    data_split = [row for row in csvreader(data)]

    return data_split

########################################## UPDATE WINDOW ##########################################

def update_window(window, loc_data_dict, chosen_locations, settings):
    MAX_ROWS, MAX_COLS = int(settings['rows']), int(settings['cols'])
    show = chosen_locations
    for i, loc in enumerate(show):
        if loc == '-DRILLDOWN-':
            continue
        if i >= MAX_COLS * MAX_ROWS:
            break
        values = loc_data_dict[(loc, 'Total')]
        window[f'-TITLE-{i}'].update(f'{loc} {max(values)}')
        graph = window[i]
        # auto-scale the graph.  Will make this an option in the future
        max_value = max(values)
        graph.change_coordinates((0, 0), (DATA_SIZE[0], max_value))
        # calculate how big the bars should be
        num_values = len(values)
        bar_width_total = DATA_SIZE[0] // num_values
        bar_width = bar_width_total * 2 // 3
        bar_width_spacing = bar_width_total
        # Draw the Graph
        graph.erase()
        bar_ids = [graph.draw_rectangle(top_left=(i * bar_width_spacing + EDGE_OFFSET, graph_value),
                                        bottom_right=(i * bar_width_spacing + EDGE_OFFSET + bar_width, 0),
                                        line_width=0,
                                        fill_color=sg.theme_text_color()) for i, graph_value in enumerate(values)]

    window['-UPDATED-'].update('Updated ' + datetime.now().strftime("%B %d %I:%M:%S %p") + f'\nDate of last datapoint {date_of_final_datapoint}')

########################################## MAIN ##########################################


##############################################################
# Data Format of CSV File                                    #
#   0                   1       2         3       4      5   #
# State/Province    Country     Lat     Long    1/22    1/23 #
##############################################################

def prepare_data():
    """
    Downloads the CSV file and creates a dictionary containing the data
    Dictionary:      Location (str,str) : Data [ int, int, int, ...  ]
    :return:        Dict[(str,str):List[int]]
    """
    global date_of_final_datapoint

    data = download_data()
    header = data[0]
    date_of_final_datapoint = header[-1]
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

    return loc_data_dict


def create_window(settings):
    MAX_ROWS = int(settings['rows'])
    MAX_COLS = int(settings['cols'])
    # Create grid of Graphs with titles
    graph_layout = [[]]
    for row in range(MAX_ROWS):
        graph_row = []
        for col in range(MAX_COLS):
            graph = sg.Graph(GRAPH_SIZE, (0,0), DATA_SIZE, key=row*MAX_COLS+col, pad=(0,0))
            graph_row += [sg.Col([[sg.T(size=(15,1), key=f'-TITLE-{row*MAX_COLS+col}')],[graph]], pad=(0,0))]
        graph_layout += [graph_row]

    # Create the layout
    layout = [[sg.T('×', font=('Arial Black', 16), enable_events=True, key='-QUIT-'),
               sg.Text('COVID-19 Cases By Region', font='Any 20'),],]
    layout += graph_layout
    layout += [ [sg.T(size=(80,2), font='Any 8', key='-UPDATED-')],
                [sg.T('Settings', key='-SETTINGS-', enable_events=True),
                 sg.T('Refresh', key='-REFRESH-', enable_events=True),
                 sg.T('Exit', key='Exit', enable_events=True),]]

    window = sg.Window('COVID-19 Confirmed Cases', layout, grab_anywhere=True, no_titlebar=False, margins=(0,0), finalize=True)

    return window

def main(refresh_minutes):
    settings = load_settings()
    sg.theme(settings['theme'])
    loc_data_dict = prepare_data()
    keys = loc_data_dict.keys()
    countries = set([k[0] for k in keys])
    # chosen_locations = choose_locations(loc_data_dict.keys())
    chosen_locations = choose_locations(countries)

    window = create_window(settings)

    update_window(window, loc_data_dict, chosen_locations, settings)

    while True:         # Event Loop
        event, values = window.read(timeout=refresh_minutes*60*1000)
        if event in (None, 'Exit', '-QUIT-'):
            break
        if event == '-SETTINGS-':
            settings = change_settings(settings)
            sg.theme(settings['theme'] if settings.get('theme') else sg.theme())
            window.close()
            window = create_window(settings)
        sg.popup_quick_message('Updating data', font='Any 20')
        loc_data_dict = prepare_data()
        update_window(window, loc_data_dict, chosen_locations, settings)

    window.close()



if __name__ == '__main__':
    main(refresh_minutes=20)
