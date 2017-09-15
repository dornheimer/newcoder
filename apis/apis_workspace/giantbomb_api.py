import requests

class GiantBombAPI:
    """
    Very simple implementation of the Giantbomb API that only offers the
    GET /platforms/ call as a generator.

    Note that this implementation only exposes of the API what we really need.
    """

    base_url = 'http://www.giantbomb.com/api'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_platforms(self, sort=None, data_filter=None, field_list=None):
        """Generator yielding platforms matching the given criteria.

        If no limit is specified,  this will return *all* platforms.
        """
        # Convert data format to what the API requires
        params = {}
        if sort is not None:
            params['sort'] = sort
        if field_list is not None:
            params['field_list'] = ','.join(field_list)
        if data_filter is not None:
            parsed_filters = [f'{k}:{v}' for k, v in data_filter.items()]
            params['filter'] = ','.join(parsed_filters)

        params['api_key'] = self.api_key
        params['format'] = 'json'

        incomplete_result = True
        num_total_results = None
        num_fetched_results = 0
        counter = 0

        while incomplete_result:
            # GB has limit of 100 items per call
            params['offset'] = num_fetched_results
            result = requests.get(self.base_url + '/platforms/',
                                    params=params).json()

            if num_total_results is None:
                num_total_results = int(result['number_of_total_results'])
            num_fetched_results += int(result['number_of_page_results'])
            if num_fetched_results >= num_total_results:
                incomplete_result = False

            for item in result['results']:
                logging.debug("Yielding platform {counter+1} of {num_total_results}")

                if item.get('original_price'):
                    item['original_price'] = float(item['original_price'])

                yield item
                counter += 1
