from datetime import datetime

from .animals_data_comparer import determine_database_actions
from .database_actions import DatabaseActions
from dynamodb_management import DynamodbManager
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

        animals_to_add = {pf_animals[id_] for id_ in db_actions[DatabaseActions.SHOULD_ADD]}
        self.dynamodb_manager.add_animals(animals_to_add)

        animals_to_remove = {db_animals[id_] for id_ in db_actions[DatabaseActions.MARK_REMOVED]}
        self.dynamodb_manager.mark_animals_removed(animals_to_remove)

        for id_ in db_actions[DatabaseActions.CHANGE_STATUS]:
            animal = pf_animals[id_]
            self.dynamodb_manager.change_parameter(
                animal=animal,
                **{PetfinderParameters.STATUS.value: getattr(animal, PetfinderParameters.STATUS.value)}
            )

        for id_ in db_actions[DatabaseActions.CHANGE_ORG_ID]:
            animal = pf_animals[id_]
            self.dynamodb_manager.change_parameter(
                animal=animal,
                **{PetfinderParameters.ORGANIZATION_ID.value: getattr(animal, PetfinderParameters.ORGANIZATION_ID.value)}
            )
