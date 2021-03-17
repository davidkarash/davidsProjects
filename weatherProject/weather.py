"""Code for Project 01 - Weather Stats.

Uses weeklong data from LAX, and monthlong data from MIA.
"""


import sys

from typing import List, Tuple
from csv import DictReader


__author__ = "730407523"


READ_ONLY = "r"
UTF8 = "UTF8"
VALID_OPS: List[str] = [
    "list",
    "min",
    "max",
    "avg",
    "chart"
]
DATE_LOWER = 5  # Gives lower bound for date length (0-10 will give full date, 5-10 will give just MM/DD)
DATE_UPPER = 10  # Gives upper bound for date length
REPORT_TYPE_LOOKUP = "SOD  "
REPORT_TYPE = "REPORT_TYPE"
DATE = "DATE"


def main() -> None:
    """Entrypoint of program."""
    if len(sys.argv) != 4 or sys.argv[1][(len(sys.argv[1]) - 4):(len(sys.argv[1]))] != ".csv":
        print("Usage: python -m projects.pj01.weather [FILE] [COLUMN] [OPERATION]")
        exit()
    elif not sys.argv[3] in VALID_OPS:
        print("Invalid operation: " + sys.argv[3])
        exit()
    results_and_dates: Tuple[List[float], List[str]] = list()
    if sys.argv[3] == "list":
        print(results_and_dates[0])
    elif sys.argv[3] == "min":
        print(min(results_and_dates[0]))
    elif sys.argv[3] == "max":
        print(max(results_and_dates[0]))
    elif sys.argv[3] == "avg":
        print(sum(results_and_dates[0]) / len(results_and_dates[0]))
    elif sys.argv[3] == "chart":
        chart_data(results_and_dates[0], sys.argv[2], results_and_dates[1])
    return None
    
    
def list() -> Tuple[List[float], List[str]]:
    """Creates 2 lists of data from data given at command line and returns them in a Tuple.

    The first list contains float values from the column given at command line.
    The second list contains reformatted dates from the dates column.
    """
    file_handle = open(sys.argv[1], READ_ONLY, encoding=UTF8)
    csv_reader = DictReader(file_handle)
    results_list: List[float] = []
    dates_list: List[str] = []
    ref_dates_list: List[str] = []

    # Collect data
    for row in csv_reader:
        if row[REPORT_TYPE] == REPORT_TYPE_LOOKUP:
            try:
                results_list.append(float(row[sys.argv[2]]))
                dates_list.append(row[DATE])
            except ValueError:  # Ignore ValueError
                ...
            except KeyError:  # Print error and exit program for KeyError
                print("Invalid column: " + sys.argv[2])
                exit()
    
    # Reformat dates
    i: int
    for date in dates_list:
        new_date = ""
        i = 0
        for i in range(DATE_LOWER, DATE_UPPER):
            new_date += date[i]
        ref_dates_list.append(new_date)

    file_handle.close()
    return (results_list, ref_dates_list)


def chart_data(data: List[float], column: str, dates: List[str]):
    """Charts data against dates in a line graph."""
    import matplotlib.pyplot as plt
    plt.title(sys.argv[2] + " from " + dates[0] + " to " + dates[len(dates) - 1])
    plt.plot(dates, data)
    plt.xticks(rotation=90, fontsize=8)
    plt.xlabel(DATE)
    plt.ylabel(column)
    plt.show()


if __name__ == "__main__":
    main()