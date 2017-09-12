"""
Data Visualization Project

Parse data from an ugly CSV or Excel file, and render it in
JSON-like form, visualize in graphs, and plot on Google Maps.

Part II: Take the data we just parsed and visualize it using popular
Python math libraries.
"""

from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

from parse import parse


MY_FILE = "../data/sample_sfpd_incident_all.csv"
DATA = parse(MY_FILE, ",")


def visualize_days(parsed_data):
    """Visualize data by day of week."""
    # Returns a dict where it sums the total values for each key.
    # In this case, the keys are the DaysOfWeek, and the values are
    # a count of incidents.
    counter = Counter(item["DayOfWeek"] for item in parsed_data)

    # Separate out the counter to order it correctly when plotting.
    data_list = [
                  counter["Monday"],
                  counter["Tuesday"],
                  counter["Wednesday"],
                  counter["Thursday"],
                  counter["Friday"],
                  counter["Saturday"],
                  counter["Sunday"]
                ]
    day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])

    # Assign the data to a plot
    plt.plot(data_list)

    # Assign labels to the plot from day_list
    plt.xticks(range(len(day_tuple)), day_tuple)

    # Save the graph!
    # If you look at new-coder/dataviz/tutorial_source, you should see
    # the PNG file, "Days.png".  This is our graph!
    plt.savefig("Days.png")

    # Close figure
    plt.clf()


def visualize_type(parsed_data):
    """Visualize data by category in a bar graph."""
    # Same as before, this returns a dict where it sums the total
    # incidents per Category.
    counter = Counter(item["Category"] for item in parsed_data)

    # Set the labels which are based on the keys of our counter.
    labels = tuple(counter.keys())

    # Set where the labels hit the x-axis
    xlocations = np.arange(len(labels)) + 0.5

    # Width of each bar
    width = 0.5

    # Assign data to a bar plot
    plt.bar(xlocations, counter.values(), width=width)

    # Assign labels and tick location to x-axis
    plt.xticks(xlocations + width / 2, labels, rotation=90)

    # Give some more room so the labels aren't cut off in the graph
    plt.subplots_adjust(bottom=0.4)

    # Make the overall graph/figure larger
    plt.rcParams['figure.figsize'] = 12, 8

    # Save the graph!
    # If you look at new-coder/dataviz/tutorial_source, you should see
    # the PNG file, "Type.png".  This is our graph!
    plt.savefig("Type.png")

    # Close figure
    plt.clf()


def main():

    visualize_days(DATA)
    visualize_type(DATA)


if __name__ == "__main__":
    main()
