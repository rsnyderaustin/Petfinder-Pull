import json
import requests
import time

from petfinder_enums import PetfinderParameters


def _determine_num_of_pages(pf_json):
    data = json.loads(pf_json)
    num_pages = data['pagination']['total_pages']
    return num_pages


def _include_category_in_url(url, category):
    if not url.endswith('/'):
        url += '/'

    return f"{url}{category}"


class PetfinderApiPull:

    def __init__(self, access_token: str, data_url: str, category: str, **params):
        self.access_token = access_token
        self.data_url = _include_category_in_url(url=data_url, category=category)
        self.params = params

        self.num_pages = 999999
        self.page_num = 1

        self.data = []

    def _pull_page(self, page_num, **params) -> requests.Response:

        header = {
            'Authorization': f'Bearer {self.access_token}'
        }
        page_params = {
            **params,
            'page': page_num,
            'limit': 100
        }
        response = requests.get(self.data_url, headers=header, params=page_params)

        response.raise_for_status()

        return response

    def pull_data(self, **params):
        while self.num_pages > self.page_num and self.page_num < 500:
            page_response = self._pull_page(
                page_num=self.page_num,
                **params
            )
            json_ = page_response.json()
            self.data.extend(json_['animals'])

            # If this is the first page then establish the number of pages for the rest of the pull
            if self.page_num == 1:
                self.num_pages = json_['pagination']['total_pages']

            self.page_num += 1
            time.sleep(0.04)

        return self.pull_data
