import logging
import requests


CPI_DATA_URL = 'http://research.stlouisfed.org/fred2/data/CPIAUCSL.txt'


class CPIData:
    """Abstraction of the CPI data provided by FRED.

    This stores internally only one value per year.
    """

    def __init__(self):
        self.year_cpi = {}
        self.last_year = None
        self.first_year = None

    def load_from_url(self, url, save_as_file=None):
        """Load data from a given URL.

        The downloaded file can also be saved into a location for later
        re-use with the "save_as_file" parameter specifying a file name.

        After fetching the file this implementation uses load_from_file
        internally.
        """
        fp = requests.get(url, stream=True,
                            headers={'Accept Encoding': None})

        if save_as_file is None:
            return self.load_from_file(fp)

        else:
            with open(save_as_file, 'wb') as out:
                for chunk in fp.iter_content(chunk_size=128):
                    out.write(chunk)
            with open(save_as_file) as fp:
                return self.load_from_file(fp)

    def load_from_file(self, fp):
        """Load CPI data from a given file-like object."""
        current_year = None
        cpis_year = []

        # Skip until header line
        for line in fp:
          if line.startswith("DATE"):
              break

        for line in fp:
            # Remove trailing newline char and split line
            data = line.rstrip().split()
            year = int(data[0].split("-")[0]) # Only get year
            cpi = float(data[1])

            if self.first_year is None:
                self.first_year = year
            self.last_year = year

            # The moment we reach a new year, we have to reset the CPI data
            # and calculate the average CPI of the current_year
            if current_year != year:
                if current_year is not None:
                    self.year_cpi[current_year] = sum(cpis_year) / len(cpis_year)
                cpis_year = []
                current_year = year
            cpis_year.append(cpi)

        # calculation for last year (no new year after to initialize computation above)
        if current_year is not None and current_year not in self.year_cpi:
            self.year_cpi[current_year] = sum(cpis_year) / len(cpis_year)


    def get_adjusted_price(self, price, year, current_year=None):
        """Return the adapted price from a given year compared to what current
        year has been specified.
        """
        # if our data range doesnt provide a CPI for the given year, use
        # the edge data
        if year < self.first_year:
            year = self.first_year
        elif year > self.last_year:
            year = self.last_year

        year_cpi = self.year_cpi[year]
        current_cpi = self.year_cpi[current_year]

        return float(price) * (current_cpi / year_cpi)
