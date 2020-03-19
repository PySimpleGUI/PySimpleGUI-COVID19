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

![image](https://user-images.githubusercontent.com/46163555/77016602-83556a00-694e-11ea-8020-6e57f5176338.png)



This is an exciting little piece of software.  It's much like a grid of graphs that Tableau creates.  This format is a fantastic way to display datasets in a way that can be quickly and easily compared visually.

Rather than using Matplotlib or any other graphing packages, this program uses PySimpleGUI's built-in drawing primitives.  

### Choose Locations

The locations are pulled from the file containing the detailed data and displayed as a window full of checkboxes.  

![image](https://user-images.githubusercontent.com/46163555/77016687-ce6f7d00-694e-11ea-8b30-8d9eee055e40.png)


### Settings

In addition to being able to chose the locations to display, you can also set:

* The PySimpleGUI Color Theme
* Number of graphs (rows and columns)
* Scaling - autoscaled or scale to a particular value


#### Scaling

You can now choose either autoscalled graphs or set them all to have the same maximum value.  If autoscale is chosen, then each graph's Y Axis has a maximum value that's the same as the maxiumum value in that graph's data.

Setting the value to be a fixed number instead of a autoscalled enables country to country comparisons.  It's in the non-scalled view that you can see the wave of infections sweep over the Earth, each country starting at a slightly different time than the others.  

![image](https://user-images.githubusercontent.com/46163555/77016721-e0512000-694e-11ea-9fd9-e8465ba7854a.png)


#### Number of Graphs

You can make your window contain as many graphs as you have room for on your screen.  Here's a window with 36 instead of the default 16.

![image](https://user-images.githubusercontent.com/46163555/77016914-679e9380-694f-11ea-8085-49e774d87a74.png)



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

Have a suggestion?  Open an Issue with your ideas.

At the moment, the focus is on expanding this software using a design I've already created rather than rolling in suggested changes by other people.  Feel free to folk the repo and go crazy.  Please understand that submitting a change doesn't mean it'll be automatically accepted.  If it's not and you think you'll be upset, then perhaps skip submitting it.



--------------------------------

Copyright 2020 PySimpleGUI.com

