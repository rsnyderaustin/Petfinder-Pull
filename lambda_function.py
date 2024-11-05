import boto3
from botocore.config import Config
import os

from dynamodb_management import DynamodbManager
import petfinder_api
from petfinder_api import PetfinderApiManager

retry_config = Config(
    retries={
        'mode': 'standard'
    }
)

in_aws = bool(os.getenv("AWS_EXECUTION_ENV"))

if not in_aws:
    from dotenv import load_dotenv
    load_dotenv()


def lambda_handler():
    api_key = os.getenv('PF_API_KEY')
    secret_key = os.getenv('PF_SECRET_KEY')
    data_url = os.getenv('PF_DATA_REQUEST_URL')
    token_url = os.getenv('PF_ACCESS_TOKEN_URL')
    dynamodb_table_name = os.getenv('PF_DYNAMODB_TABLE_NAME')
    pf_api_manager = PetfinderApiManager(
        api_key=api_key,
        secret_key=secret_key,
        data_url=data_url,
        token_url=token_url
    )

    dynamodb_manager = DynamodbManager(table_name=dynamodb_table_name)

    animals = {}

    dog_data = pf_api_manager.get_from_api(category='animals',
                                           type='dog')
    for id_, data in dog_data.items():
        new_animal = petfinder_api.create_animal(**data)
        animals[id_] = new_animal

    cat_data = pf_api_manager.get_from_api(category='animals',
                                           type='cat')
    for id_, data in cat_data.items():
        new_animal = petfinder_api.create_animal(**data)
        animals[id_] = new_animal


if not in_aws:
    lambda_handler()


