import json
import requests
import time
from typing import Callable

from .petfinder_access_token import PetfinderAccessToken
from .petfinder_json_parser import fetch_animals_data, fetch_number_of_pages


def _include_category_in_url(url, category):
    if not url.endswith('/'):
        url += '/'

    return f"{url}{category}"


class PetfinderApiPull:

    def __init__(self, access_token: PetfinderAccessToken, data_url: str, category: str, **params):
        self.access_token = access_token
        self.data_url = _include_category_in_url(url=data_url, category=category)
        self.params = params

        self.num_pages = 1e10
        self.page_num = 1

        self.data = []

    def _pull_page(self, page_num, **params) -> requests.Response:

        header = {
            'Authorization': f'Bearer {self.access_token.access_token}'
        }
        page_params = {
            **params,
            'page': page_num,
            'limit': 100
        }
        response = requests.get(self.data_url, headers=header, params=page_params)

        response.raise_for_status()

        return response

    def pull_data(self, new_access_token_func: Callable, **params):
        while self.num_pages >= self.page_num and self.page_num < 500:
            if self.access_token.should_replace:
                self.access_token = new_access_token_func()

            page_response = self._pull_page(
                page_num=self.page_num,
                **params
            )
            json_ = page_response.json()

            animals_data = fetch_animals_data(json_)
            self.data.extend(animals_data)

            # If this is the first page then establish the number of pages for the rest of the pull
            if self.page_num == 1:
                self.num_pages = fetch_number_of_pages(json_)

            self.page_num += 1

            # Rate limit for Petfinder API calls
            time.sleep(0.04)

        return self.pull_data
