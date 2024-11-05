import boto3

from .dynamodb_parameters import DynamodbParameters
from animals import Animal
from petfinder_enums import PetfinderParameters, PetfinderValues


class DynamodbManager:

    def __init__(self, table_name: str, pull_timestamp: str):
        self.pull_timestamp = pull_timestamp

        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(table_name)

    def get_animals(self) -> dict:
        response = self.table.scan(
            ProjectExpression=f"{PetfinderParameters.ANIMAL_ID}, #status, #org_id",
            ExpressionAttributeNames={
                '#status': PetfinderParameters.STATUS,
                '#org_id': PetfinderParameters.ORGANIZATION_ID
            }
        )
        items = response.get('Items', [])

        while 'LastEvaluatedKey' in response:
            response = self.table.scan(
                ProjectExpression=f"{PetfinderParameters.ANIMAL_ID}, #status",
                ExpressionAttributeNames={
                    '#status': PetfinderParameters.STATUS,
                    '#org_id': PetfinderParameters.ORGANIZATION_ID
                },
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items.extend(response.get('Items', []))

        animals = {}
        for item in items:
            animals[item[PetfinderParameters.ANIMAL_ID]] = Animal(
                animal_id=PetfinderParameters.ANIMAL_ID,
                org_id=PetfinderParameters.ORGANIZATION_ID,
                status=PetfinderParameters.STATUS
            )

        return animals

    def add_animals(self, animals):
        with self.table.batch_writer() as batch_w:
            for animal in animals:
                item = {
                    **animal.__dict__,
                    DynamodbParameters.TIMESTAMP.value: self.pull_timestamp
                }
                batch_w.put_item(Item=item)

    def mark_animals_removed(self, animals):
        with self.table.batch_writer() as batch_w:
            for animal in animals:
                item = {
                    PetfinderParameters.ANIMAL_ID.value: animal.animal_id,
                    DynamodbParameters.TIMESTAMP.value: self.pull_timestamp,
                    PetfinderParameters.STATUS.value: PetfinderValues.STATUS_REMOVED.value
                }
                batch_w.put_item(Item=item)

    def change_parameter(self, animal, **parameters):
        item = {
            PetfinderParameters.ANIMAL_ID.value: getattr(animal, PetfinderParameters.ANIMAL_ID.value),
            DynamodbParameters.TIMESTAMP.value: self.pull_timestamp,
            **parameters
        }
        self.table.put_item(
            Item=item
        )
