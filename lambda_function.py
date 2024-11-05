from botocore.config import Config
import os

import program_management

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
    
    prog_manager = program_management.ProgramManager(
        api_key=api_key,
        secret_key=secret_key,
        data_request_url=data_url,
        token_url=token_url,
        dynamodb_table_name=dynamodb_table_name
    )
    prog_manager.update_database()


if not in_aws:
    lambda_handler()


