import argparse
import logging
import matplotlib.pyplot as plt
import numpy as np
import tablib


def is_valid_dataset(platform):
    """Filter out datasets that are unusable.

    Return False if platform is missing 'release_date ', 'original_price',
    'name', or 'abbreviation'."""
    if not platform.get('release_date'):
        logging.warn(f'{platform['name']} has no release date.')
    if not platform.get('original_price'):
        logging.warn(f'{platform['name']} has no original_price.')
    if not platform.get('name'):
        logging.warn('No platform name for given dataset.')
    if not platform.get('abbreviation'):
        logging.warn(f'{platform['name']} has no abbreviation.')

    return True


def generate_plot(platforms, output_file):
    """Generate a bar chart out of the given platforms and writes the output
    into the specified file as PNG image.
    """
    # convert platforms into format that can be used in the plot
    labels = []
    values = []
    for platform in platforms:
        name = platform['name']
        adjusted_price = platform['adjusted_price']
        price = platform['original_price']

        # skip prices that are too high
        if price > 2000:
            continue

        # if name is too long, replace with abbreviation
        if len(name) > 15:
            name = platform['abbreviation']

        labels.insert(0, f'{name}\n$ {price}\n$ {round(adjusted_price, 2)}')
        values.insert(0, adjusted_price)

    width = 0.3
    ind = np.arange(len(values))
    fig = plt.figure(figsize=(len(labels)) * 1.8, 10)

    ax = fig.add_subplot(1, 1, 1)
    ax.bar(ind, values, width, align='center')

    plt.ylabel('Adjusted price')
    plt.xlabel('Year / Console')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(labels)
    fig.autofmt_xdate()
    plt.grid(True)

    plt.savefig(output_file, dpi=72)


def generate_csv(platforms, output_file):
    """Write the given platforms into a CSV file specified by output_file.

    The output file can either be the path to a file or a file-like object.
    """
    dataset = tablib.Dataset(headers=['Abbreviation', 'Name', 'Year', 'Price',
                                        'Adjusted price'])

    for p in platforms:
        dataset.append([p['abbreviation'], p['name'], p['year'],
                        p['original_price'], p['adjusted_price']])

    if isinstance(output_file, basestring):
        with open(output_file, 'w+') as fp:
            fp.write(dataset.csv)
    else:
        output_file.write(dataset.csv)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument
