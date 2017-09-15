from cpi_data import CPIData
from giantbomb_api import GiantBombAPI
from helper_functions import is_valid_dataset, generate_csv, generate_plot, parse_args


CPI_DATA_URL = 'http://research.stlouisfed.org/fred2/data/CPIAUCSL.txt'


def main():
    """This function handles the actual logic of this script."""

    # Grab CPI/Inflation data
    cpi_data = CPIData()
    cpi_data.load_from_url(CPI_DATA_URL, 'cpi_data.txt')

    # Grab API/game platform data
    api_key = 'cc774dd2100b8ac804f14b4354bedbfdbe51433d'
    giantbomb_api = GiantBombAPI(api_key=api_key)

    sort = "'release_date':asc"
    data_filter = {}
    field_list = ['abbreviation', 'name', 'original_price', 'release_date']
    platform_data = giantbomb_api.get_platforms(data_filter=data_filter,
                                                field_list=field_list)

    # Figure out the current price of each platform
    for p in platform_data:
        if giantbomb_api.is_valid_dataset(p):
            p['adjusted_price'] = cpi_data.get_adjusted_price(p['price'], p['year'],
                                                                current_year=2017)

    # Generate a plot/bar graph for the adjusted price data
    generate_plot(platform_data, 'giantbomb.png')
    # Generate a CSV file to save the adjusted price data
    generate_csv(platform_data, 'giantbomb.csv')
