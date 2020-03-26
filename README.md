# PySimpleGUI-COVID19
A collection of PySimpleGUI based tools to help analyze the spread of the COVID-19 virus

The Johns Hopkins GitHub repository and dataset has become an amazing resource for anyone wishing to get detailed information about the COVID-19 situation.

The source data for these can be found here:

https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series


## Tools

There are currently 2 tools checked in.  


1 - The COVID-19 Distance Widget that is from the PSG-Widgets repository

2 - The COVID-19 Confirmed Cases Graphs


## Requirements

### Running The .py Files

If you want to run the Python code, you need to install PySimpleGUI.  You'll also need geopy if you want to run the Widget.

These are easily installable via pip.

### EXE Files

If you don't want to bother with setting up a Python environment and just want to run the programs by themselves, then you'll find EXE files in this GitHhub.  The EXE files were created using the PySimpleGUI-exemaker program (available via pip).  It uses pyinstaller as described in the PySimpleGUI documentation.

# COVID-19 Grid of Graphs Interactive Data Display



## Introduction


Viewing multiple series of data as a grid of graphs enables the viewer to quickly and easily get both the big picture as well as information on indivdual countries.  It's much like the way Tableau displays data.

Rather than using Matplotlib or any other graphing packages, this program uses PySimpleGUI's built-in drawing primitives. The code to create a graph is literally a couple of lines of code.  One is a for-each statement that forms the loop, the other line of code draws the bars.

This program uses the Johns Hopkins Time-Series data that is posted here:

![SNAG-0711](https://user-images.githubusercontent.com/46163555/77267769-0b52b100-6c7a-11ea-8ac2-e39172ebcb76.jpg)

Two files are used, one for confirmed cases, the other for deaths.

Each graph displays a header that shows the country name, the number of new cases/deaths in the last data point and the % increase this value represents.

![image](https://user-images.githubusercontent.com/46163555/77251392-770a2f00-6c24-11ea-8bb3-0ea27f19b181.png)


## First Run

The first time you run the program it will create a default config file.  You will be shown the "settings" and the "choose locations" windows.  Any time you change the settings / locations, your choices will be saved in the file named C19-Graph.cfg.  This file is a JSON file.  If it gets corrupted (it shouldn't), delete it and run the program again to create a new one.

## Locations

The country list is generated from the data file.  Choose the locations you want to graph using this GUI window.  Make sure the number of graphs you configure in your settings is large enough to hold your chosen countries.  The default setting is 8 graphs - 4 columns in 2 rows.


![image](https://user-images.githubusercontent.com/46163555/77251371-55a94300-6c24-11ea-9c4f-8d412fa164e1.png)


## Settings

In addition to being able to chose the locations to display, you can also set:

* The data to display - confirmed cases or deaths
* The PySimpleGUI Color Theme
* Number of graphs (rows and columns)
* The size of each graph in pixels
* Scaling - autoscaled or scale to a particular value
* Number of days to display

![SNAG-0703](https://user-images.githubusercontent.com/46163555/77251115-d7986c80-6c22-11ea-966b-2c575c31df75.jpg)

## Displaying Current Values

The default view displays only the current values and has autoscaling initially enabled.  Autoscaling will set each graph's max Y value to the max value found in the data for the country.  All graphs will be the same height when autoscaled.  Autoscaled graphs enable you to easily compare the 'shape' of the curves.  

![SNAG-0713](https://user-images.githubusercontent.com/46163555/77267776-0ee63800-6c7a-11ea-9871-9436bc125188.jpg)


When autoscaling is turned off the absolute values for each country are displayed. This enables you to see which countries have more cases than the other countries.  It's immediately evident that Italy has the most cases in this graph.

![SNAG-0715](https://user-images.githubusercontent.com/46163555/77267912-83b97200-6c7a-11ea-8a29-2f48f0c2f604.jpg)



## Scrolling Through Historical Data

Use the slider labeled "Way back machine" to adjust the range of dates that are displayed.  The very top of the window displays the range being shown.  By stepping the slider one day at a time you can watch the changes over time. 

In this graph the data has been rewound 7 days and shows at the top that 2/14/20 to 3/15/20 are displayed:

![SNAG-0714](https://user-images.githubusercontent.com/46163555/77267772-0d1c7480-6c7a-11ea-91e5-17a98bbfe93b.jpg)


## Predicting The Future

***Caution Advised*** - The prediction feature is based on a simple exponential growth formula.  You have control over the growth rate which has a default value of 1.25.  This means that each day's change will be 1.25 times the prior day's change.  It's meant to help inform you of ***one possible outcome*** among many.  

One thing that is become clear, it's the citizens in each country that has direct control over how quickly and how much the virus spreads.  You as an individual have the potential to help or hurt your local population.  Each person that gets the virus spreads it to 2 to 3 people.  By staying home, away from other people, you reduce both the chance you catch the virus and the number of other people you potentially expose if you are infected.

Predicted values are shown in red.

Use the "Enable Forecasting" checkbox on the main window to enable forecasting.  Then use the slider to change the number of days into the future to predict. As mentioned previously, you can change the default growth rate of 1.25 to any value.  When you enable forecasting, the number of rows in your window will double.  If you disable forecasting, the number of rows will halve.  Be sure you have enough graphs configured in your settings to display all of the countries you selected.

This graph is showing the predicted number of deaths 7 days into the future.

![SNAG-0711](https://user-images.githubusercontent.com/46163555/77267769-0b52b100-6c7a-11ea-8ac2-e39172ebcb76.jpg)


## As Many As You Want

Want to see 81 countries in 1 shot?   No problem.  The limit on the number of graphs is limited only by how much data is available.  If you have a large enough display then you can easily create a 200 or more graph display. 

The big picture is that we're all in the exact same virus infested boat.

The lessons learned will be from each other.

![SNAG-0725](https://user-images.githubusercontent.com/46163555/77491445-29ecaf80-6e14-11ea-829b-f3b3265a8da0.jpg)



-----------------------------



## The Distance Tracker

This was the first of these tools developed and was publised in the PSG Widgets Repo first.


![SNAG-0527](https://user-images.githubusercontent.com/46163555/76657707-dc855e00-6548-11ea-89cd-7c9f6b28978a.jpg)


------------------------

# NOTES

This may be the first major health crisys captured in this much detail and made available widely to the research community / public.  It'll be the best documented and will make post-mortems much easier to perform down the road when we piece together "what really happened". 

## STAY SAFE

## Listen to reputable news stations for information

## Stay away from information sources that are not scientifically verified to be true

## The WHO is the most trustworthy information at this time (most likely)

https://www.who.int/emergencies/diseases/novel-coronavirus-2019

[Download their daily PDF files](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports) that have the "Situation Report" for the most up to date information.


# Contributing

Have a suggestion?  Open an Issue with your ideas.

At the moment, the focus is on expanding this software using a design I've already created rather than rolling in suggested changes by other people.  Feel free to folk the repo and go crazy.  Please understand that submitting a change doesn't mean it'll be automatically accepted.  If it's not and you think you'll be upset, then perhaps skip submitting it.



--------------------------------

Copyright 2020 PySimpleGUI.com

