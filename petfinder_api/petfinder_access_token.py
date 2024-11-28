
import time


class PetfinderAccessToken:

    def __init__(self, access_token_json):
        self.expires_in = access_token_json.get('expires_in')
        self.access_token = access_token_json.get('access_token')

    def __post_init__(self):
        current_time = time.time()
        self.expires_at = current_time + self.expires_in

    @property
    def should_replace(self):
        one_minute_before_expiration = self.expires_in - 60
        current_time = time.time()
        return current_time >= one_minute_before_expiration

