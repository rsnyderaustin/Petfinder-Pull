from enum import Enum


class PetfinderParameters(Enum):
    ANIMAL_ID = 'id'
    TYPE = 'type'
    STATUS = 'status'
    ORGANIZATION_ID = 'organization_id'


class PetfinderValues(Enum):
    STATUS_ADOPTED = 'adopted'
    STATUS_ADOPTABLE = 'adoptable'
    STATUS_REMOVED = 'removed'
