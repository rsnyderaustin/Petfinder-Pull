import json
import requests


def _determine_num_of_pages(pf_json):
    data = json.loads(pf_json)
    num_pages = data['pagination']['total_pages']
    return num_pages


class PetfinderApiPull:

    def __init__(self, access_token: str, host_url: str, **params):
        self.access_token = access_token
        self.host_url = host_url
        self.params = params

        self.num_pages = None
        self.page_num = 1

        self.pull_data = []

    def _pull_page(self, page_num, **params):

        header = {
            'Authorization': f'Bearer {self.access_token}'
        }
        page_params = {
            **params,
            'page': page_num
        }
        response = requests.get(self.host_url, headers=header, data=page_params)

        response.raise_for_status()

        return response.json()

    def pull_data(self, **params):
        while not self.num_pages > self.page_num and self.page_num < 500:
            page_json = self._pull_page(
                page_num=self.page_num,
                **params
            )
            page_data = json.loads(page_json)['animals']
            self.pull_data.extend(page_data)

            # If this is the first page then establish the number of pages for the whole pull
            if self.page_num == 1:
                self.num_pages = _determine_num_of_pages(page_json)

            self.page_num += 1

        return self.pull_data
