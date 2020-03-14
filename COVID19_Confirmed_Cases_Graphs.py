import PySimpleGUI as sg
from urllib import request
from csv import reader as csvreader
from json import load as jsonload
from json import dump as jsondump
from os import path

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

DEFAULT_SETTINGS = {}

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


def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        jsondump(settings, f)


def change_settings(settings):
    layout = [[sg.T('Color Theme')],
              [sg.Combo(sg.theme_list(), size=(20,20), key='-THEME-' )],
              [sg.B('Ok', border_width=0, bind_return_key=True), sg.B('Cancel', border_width=0)],]

    window = sg.Window('Settings', layout, keep_on_top=True, border_depth=0)
    event, values = window.read()
    window.close()

    if event == 'Ok':
        settings['theme'] = values['-THEME-']

    return settings

########################################## DOWNLOAD DATA ##########################################

def download_data():

    # Download and parse the CSV file
    file_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    data = [d.decode('utf-8') for d in request.urlopen(file_url).readlines()]

    # Add blank space for missing cities to prevent dropping columns
    for n, row in enumerate(data):
        data[n] = "Unknown" + row if row[0] == "," else row

    # Split each row into a list of data
    data_split = [row for row in csvreader(data)]

    return data_split


########################################## MAIN ##########################################


def main():
    data = download_data()
    header = data[0]
    graph_data = [row[4:] for row in data[1:]]
    graph_values = []
    for row in graph_data:
        for d in row:
            graph_values.append([int(d) if d!= '' else 0 for d in row])
    location = [f'{row[0]} {row[1]}' for row in data[1:]]
    # make list of countries
    locations = set([row[1] for row in data[1:]])

    loc_data_dict = {}
    data_points = len(graph_data[0])
    for loc in locations:
        totals = [0]*data_points
        for i, row in enumerate(data[1:]):
            if loc == row[1]:
                for j, d in enumerate(row[4:]):
                    totals[j] += int(d if d!= '' else 0)
        loc_data_dict[loc] = totals


    print(f'Total locations = {len(loc_data_dict)}')



    graph_list = []
    graph_layout = [[]]
    for row in range(MAX_ROWS):
        graph_row = []
        for col in range(MAX_COLS):
            graph = sg.Graph(GRAPH_SIZE, (0,0), DATA_SIZE, key=row*MAX_COLS+col, pad=(0,0))
            graph_list.append(graph)
            graph_row += [sg.Col([[sg.T(size=(15,1), key=f'-TITLE-{row*MAX_COLS+col}')],[graph]], pad=(0,0))]
        graph_layout += [graph_row]

    layout = [[sg.T('×', font=('Arial Black', 16), enable_events=True, key='-QUIT-'),
               sg.Text('COVID-19 Cases By Region', font='Any 20'),],]
    layout += graph_layout
    layout += [[sg.Button('Draw'), sg.Exit()]]

    window = sg.Window('COVID-19 Confirmed Cases', layout, grab_anywhere=True, no_titlebar=False, margins=(0,0))

    while True:
        event, values = window.read()
        if event in (None, 'Exit', '-QUIT-'):
            break

        show = ['US', 'China', 'Italy', 'Iran', 'Korea, South', 'France', 'Spain', 'Germany', 'United Kingdom', 'Japan', 'Norway', 'Switzerland', 'Sweden', 'Australia', 'Austria', 'Netherlands']
        for i, loc in enumerate(show):
            if i >= MAX_COLS*MAX_ROWS:
                break
            values = loc_data_dict[loc]
            window[f'-TITLE-{i}'].update(f'{loc} {max(values)}')
            graph = window[i]
            # auto-scale the graph.  Will make this an option in the future
            max_value = max(values)
            graph.change_coordinates((0,0), (DATA_SIZE[0], max_value))
            # calculate how big the bars should be
            num_values = len(values)
            bar_width_total = DATA_SIZE[0]//num_values
            bar_width = bar_width_total*2//3
            bar_width_spacing = bar_width_total
            # Draw the Graph
            graph.erase()
            bar_ids = [graph.draw_rectangle(top_left=(i * bar_width_spacing + EDGE_OFFSET, graph_value),
                                        bottom_right=(i * bar_width_spacing + EDGE_OFFSET + bar_width, 0),
                                        line_width=0,
                                        fill_color=sg.theme_text_color()) for i, graph_value in enumerate(values)]

    window.close()



if __name__ == '__main__':
    # settings = load_settings()
    # sg.theme(settings['theme'])
    main()
