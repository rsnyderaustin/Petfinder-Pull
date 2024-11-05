from datetime import datetime

from .animals_data_comparer import determine_database_actions
from .database_actions import DatabaseActions
from dynamodb_management import DynamodbManager, DynamodbParameters
from petfinder_api import PetfinderApiManager
from petfinder_enums import PetfinderParameters


class ProgramManager:

    def __init__(self,
                 api_key,
                 secret_key,
                 data_request_url,
                 token_url,
                 dynamodb_table_name):

        self.pf_api_manager = PetfinderApiManager(
            api_key=api_key,
            secret_key=secret_key,
            data_url=data_request_url,
            token_url=token_url
        )
        self.dynamodb_manager = DynamodbManager(
            table_name=dynamodb_table_name,
            pull_timestamp=datetime.utcnow().isoformat()
        )

    def update_database(self):
        pf_animals = self.pf_api_manager.get_animals()
        db_animals = self.dynamodb_manager.get_animals()

        db_actions = determine_database_actions(pf_animals=pf_animals, db_animals=db_animals)

        self.dynamodb_manager.add_animals({pf_animals[id_] for id_ in db_actions[DatabaseActions.SHOULD_ADD]})
        self.dynamodb_manager.mark_animals_removed({db_animals[id_] for id_ in db_actions[DatabaseActions.MARK_REMOVED]})

        for id_ in db_actions[DatabaseActions.CHANGE_STATUS]:
            self.dynamodb_manager.change_parameter(
                animal=pf_animals[id_],
                **{PetfinderParameters.STATUS.value: getattr(pf_animals[id_], PetfinderParameters.STATUS.value)}
            )

        for id_ in db_actions[DatabaseActions.CHANGE_ORG_ID]:
            self.dynamodb_manager.change_parameter(
                animal=pf_animals[id_],
                **{PetfinderParameters.ORGANIZATION_ID.value: getattr(pf_animals[id_], PetfinderParameters.ORGANIZATION_ID.value)}
            )
