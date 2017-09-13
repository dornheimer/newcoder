"""
Data Visualization Project

Parse data from an ugly CSV or Excel file, and render it in
JSON, save to a database, and visualize in graph form.

Part I: Taking data from a CSV/Excel file, and return it into a format
that is easier for Python to play with.

Copyright (c) 2013 E. Lynn Root
Distributed under the zlib png license. See LICENSE for details.
"""

import csv
import json


MY_FILE = "../data/sample_sfpd_incident_all.csv"


def parse(raw_file, delimiter):
    """Parse a raw CSV file to a JSON-line object."""
    # Open and Read CSV file
    with open(raw_file) as opened_file:
        csv_data = csv.reader(opened_file, delimiter=delimiter)
        fields = csv_data.__next__()
        parsed_data = [dict(zip(fields, row)) for row in csv_data]

    return parsed_data


def save_to_json(data, filename, indent=4):
    """Save JSON-line object to JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=indent)


def main():
    # Call our parse function and give it the needed parameters
    new_data = parse(MY_FILE, ",")

    save_to_json(new_data, "json_data.json")


if __name__ == "__main__":
    main()
