This project was created to model the spread of a virus, including immunity after a set time period.

The foundations of this project were designed by course staff of COMP110 (such as the view controller), but most of the methods, charting, and argument options were created by me.  Additional elements of the simulation (such as masks) were designed out of my curiosity to extend beyond the original scope of the course assignment.

Command line arguments allow flexibility in this project, allowing the user to either run a visual simulation or create a graph of healthy, immune, and infected individuals by running model.py instead of the entire project.  

The graph module implements an argument parser that allows customization of the simulation from the command line. Using 'python -m projects.pj02.chart help' will list out the optional arguments that can be given at runtime.  

For the visual simulation, the constants can be edited within the constants.py file, and the changes will be reflected in the simulation on the next run.  
