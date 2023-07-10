import json
import requests
import time
import os

# class for interacting with the universalis API
class Universalis:

    # constructor, if quick_start is true, then the data centers and worlds will be grabbed
    def __init__(self, quick_start=False):
        self.__rate_limit = 25
        self.__data_center = None
        self.__world = None
        self.__region = 'North-America'  # default region
        self.__log_path = os.path.realpath(os.path.dirname(__file__)) + '/log/'

        self.data_centers = None
        self.worlds = None
        self.regions = ['Japan', 'Europe',
                        'North-America', 'Oceania', 'China', '中国']

        if quick_start:
            self.get_worlds()
            self.get_data_centers()

    def __clean_url_for_logging(self, url):
        cleaned_url = url
        characters_to_remove = ['/', ':', '\\', '?', '&', '=', '%', '*']
        for character in characters_to_remove:
            cleaned_url = cleaned_url.replace(character, '_')
        return cleaned_url
    
    def __fetch_json_dict(self, url):
        self.rate_limit()
        
        # generate our logfile name and response object
        log_safe_filename = self.__log_path + self.__clean_url_for_logging(url) + '_' + str(time.time()) + '.json'
        response_object = {}

        try:
            response_text = requests.get(url).text

            with open(log_safe_filename, 'w', encoding='utf-8') as f:
                f.write(str(response_text))

            response_object = json.loads(response_text)
        except Exception as e:
            response_object = {'error': str(e)}
            print('Error fetching JSON from URL: ' + url)
            print('Error: ' + str(e))
        finally:
            return response_object

    def rate_limit(self):
        # wait for 1 / self.__rate_limit seconds
        # print("Sleeping...", end= "")
        time.sleep(1 / self.__rate_limit)
        # print("Done")

    def get_worlds(self):
        self.worlds = self.__fetch_json_dict('https://universalis.app/api/v2/worlds')
        return self.worlds

    def get_data_centers(self):
        self.data_centers = self.__fetch_json_dict('https://universalis.app/api/v2/data-centers')
        return self.data_centers

    def get_item_current_data_by_region(self, item_id):
        return self.__fetch_json_dict(f'https://universalis.app/api/v2/{self.__region}/{item_id}')
    
    def get_item_sale_history_by_region(self, item_id, entriesToReturn=25):
        return self.__fetch_json_dict(f'https://universalis.app/api/v2/history/{self.__region}/{item_id}?entriesToReturn={entriesToReturn}')
    
    def get_marketable_items(self):
        return self.__fetch_json_dict('https://universalis.app/api/v2/marketable')

    def set_region(self, region):
        if region in self.regions:
            self.__region = region
            return True
        else:
            return False
