import boto3
from botocore.config import Config

from petfinder_api import PetfinderApiManager

retry_config = Config(
    retries={
        'mode': 'standard'
    }
)

pf_api_manager = PetfinderApiManager()
dog_data = pf_api_manager.get_from_api(type='dog')
cat_data = pf_api_manager.get_from_api(type='cat')

def lambda_handler()




