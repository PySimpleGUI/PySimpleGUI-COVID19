# PySimpleGUI-COVID19
A collection of PySimpleGUI based tools to help analyze the spread of the COVID-19 virus

The Johns Hopkins GitHub repository and dataset has become an amazing resource for anyone wishing to get detailed information about the COVID-19 situation.

## Tools

There are currently 2 tools checked in.  

1 - The COVID-19 Distance Widget that is from the PSG-Widgets repository
2 - The COVID-19 Confirmed Cases Graphs

## Requirements

### Running The .py Files

If you want to run the Python code, you need to install 2 packages for these tools

1 - PySimpleGUI

2 - geopy (requireed only for the Widget)

These are easily installable via pip.

### EXE Files

If you don't want to bother with setting up a Python environment and just want to run the programs by themselves, then you'll find EXE files in thie GitHhub.  At the moment only the Widget has an EXE file.  The realtime graph of confirmed cases is going through a lot of changes / development.  An EXE file should be available for it later today.



## Graphing the Confirmed Cases

![image](https://user-images.githubusercontent.com/46163555/76657691-d2fbf600-6548-11ea-9c37-9cc08d26a67b.png)

This is an exciting little piece of software.  It's much like a grid of graphs that Tableau creates.  This format is a fantastic way to display datasets in a way that can be quickly and easily compared visually.

Rather than using Matplotlib or any other graphing packages, this program uses PySimpleGUI's built-in drawing primitives.  

Creating the bar graphs is literally 1 line of code.  It's a single list comprehension that draws each bar based on individual data points.

```python
bar_ids = [graph.draw_rectangle(top_left=(i * bar_width_spacing + EDGE_OFFSET, graph_value),
                            bottom_right=(i * bar_width_spacing + EDGE_OFFSET + bar_width, 0),
                            line_width=0,
                            fill_color=sg.theme_text_color()) for i, graph_value in enumerate(values)]

```


### Data Source

This graph is produced from this CSV file of confirmed cases.  Each other counties individual values were totalled up before displaying.  Upcoming releases have the ability to split out individual countries so that you can see the data broken out by region for that country.

https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv


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

## The WHO is the most trustworthy information at this time, most likely

https://www.who.int/emergencies/diseases/novel-coronavirus-2019

[Download their daily PDF files](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports) that have the "Situation Report" for the most up to date information.


# Contributing

The focus is on completing the implementation for the software following a completed design.  Understand that submitting a change doesn't mean it's automatically accepted or that we'll even agree on approach or ideas.  If your suggestion is not used and you believe you'll be upset by this, then save everyone the grief and don't submit it.  It's my time that has being invested in this free software.  No one is asking you to spend time working on it.


--------------------------------

Copyright 2020 PySimpleGUI.com

