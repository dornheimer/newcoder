import logging
import os

from cpi_data import CPIData, CPI_DATA_URL
from giantbomb_api import GiantBombAPI
from helper_functions import is_valid_dataset, generate_csv, generate_plot, parse_args


def main():
    """This function handles the actual logic of this script."""
    opts = parse_args()

    if opts.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    cpi_data = CPIData()
    gb_api = GiantBombAPI(api_key=opts.giantbomb_api_key)

    print("Disclaimer: This script uses data provided by FRED, Federal"
        "Reserve Economic Data, from the Federal Reserve Bank of St. Louis"
        "and Giantbomb.com:\n- {0}\n- http://www.giantbomb.com/api/\n".format(CPI_DATA_URL))

    # Grab CPI/Inflation data
    if os.path.exists(opts.cpi_file):
        with open(opts.cpi_file) as fp:
            cpi_data.load_from_file(fp)
    else:
        cpi_data.load_from_url(opts.cpi_data_url, opts.cpi_file)

    # Grab API/game platform data
    field_list = ['abbreviation', 'name', 'original_price', 'release_date']
    platform_data = gb_api.get_platforms(sort='release_date:desc',
                                            field_list=field_list)

    # Figure out the current price of each platform
    platforms = []
    counter = 0
    for platform in platform_data:
        if not gb_api.is_valid_dataset(platform):
            continue

        year = int(platform['release_date'].split("-")[0])
        price = platform['original_price']
        platform['adjusted_price'] = cpi_data.get_adjusted_price(price, year)
        platform['year'] = year
        platforms.append(platform)

        if opts.limit is not None and counter + 1 >= opts.limit:
            break
        counter += 1

    # Generate a plot/bar graph for the adjusted price data
    if opts.plot_file:
        generate_plot(platform_data, opts.plot_file)
    # Generate a CSV file to save the adjusted price data
    if opts.csv_file:
        generate_csv(platform_data, opts.csv_file)


if __name__ == "__main__":
    main()
