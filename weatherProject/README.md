This project implements csv reading in order to collect and graph data from free data available from the NOAA.  

weather.py takes input from the command line in the form of a file, a column (data type) and an operation to perform on the data.  The user can select from a list of the data, the min, max, or average, or a line chart of the data over the time period in the file.  

Graphing this data is interesting over long periods of time, where the change over time is more recognizable than the simple variance within a month or a year.  

Incorrect usage will print a usage message, and you can pull up this message from the command line using 'python -m <_path_name_> help'

A sample graph is provided in the project file, but you can add your own csv files to the project folder and then run the analysis on that data from the command line!
