from airflow.hooks.base import BaseHook
import json
import logging
import requests

from .petfinder_api_pull import PetfinderApiPull


def _determine_num_of_pages(pf_json):
    data = json.loads(pf_json)
    num_pages = data['pagination']['total_pages']
    return num_pages


class PetfinderApiResult:

    def __init__(self, json_data, pull_complete: bool):
        self.json_data = json_data
        self.pull_complete = pull_complete


class PetfinderApiManager:

    def __init__(self):
        self.conn = BaseHook.get_connection("petfinder_api")

        self.access_token = None

    def _get_api_keys(self) -> dict:
        api_key = self.conn.extradejson.get("api_key")
        api_secret = self.conn.extradejson.get("secret_api_key")

        return {
            'api_key': api_key,
            'api_secret_key': api_secret
        }

    def _get_access_token(self):
        api_keys = self._get_api_keys()
        host_url = self.conn.host
        data = {
            'grant_type': 'client_credentials',
            'client_id': api_keys['api_key'],
            'client_secret': api_keys['api_secret_key']
        }

        response = requests.post(host_url, data=data)

        response.raise_for_status()

        json_data = response.json()
        access_token = json_data.get('access_token')

        return access_token

    def get_from_api(self, **params):
        if not self.access_token:
            self.access_token = self._get_access_token()

        pf_pull = PetfinderApiPull(
            access_token=self.access_token,
            **params
        )

        try:
            data = pf_pull.pull_data(**params)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                logging.info(f"Received HTTPError 401 from Petfinder API. Getting new access token and continuing pull.")
                self.access_token = self._get_access_token()
                pf_pull.access_token = self.access_token
                data = pf_pull.pull_data(**params)
            else:
                raise http_err

        return data

