import json
import logging
import requests

from .petfinder_api_pull import PetfinderApiPull
import animals


def _determine_num_of_pages(pf_json):
    data = json.loads(pf_json)
    num_pages = data['pagination']['total_pages']
    return num_pages


class PetfinderApiResult:

    def __init__(self, json_data, pull_complete: bool):
        self.json_data = json_data
        self.pull_complete = pull_complete


class PetfinderApiManager:

    def __init__(self, data_url, token_url, api_key, secret_key):
        self.data_url = data_url
        self.token_url = token_url
        self.api_key = api_key
        self.secret_key = secret_key

        self.access_token = None

    def _get_access_token(self):

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }

        response = requests.post(self.token_url, data=data)

        response.raise_for_status()

        json_data = response.json()
        access_token = json_data.get('access_token')

        return access_token

    def get_from_api(self, category, **params):
        if not self.access_token:
            self.access_token = self._get_access_token()

        pf_pull = PetfinderApiPull(
            access_token=self.access_token,
            data_url=self.data_url,
            category=category,
            **params
        )

        try:
            data = pf_pull.pull_data(**params)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                logging.info(
                    f"Received HTTPError 401 from Petfinder API. Getting new access token and continuing pull.")
                self.access_token = self._get_access_token()
                pf_pull.access_token = self.access_token
                data = pf_pull.pull_data(**params)
            else:
                raise http_err

        return data

    def get_animals(self):
        pf_animals = {}
        dog_data = self.get_from_api(category='animals',
                                     type='dog')
        for id_, data in dog_data.items():
            new_animal = animals.create_animal(**data)
            pf_animals[id_] = new_animal

        cat_data = self.get_from_api(category='animals',
                                     type='cat')
        for id_, data in cat_data.items():
            new_animal = animals.create_animal(**data)
            pf_animals[id_] = new_animal

        return pf_animals
