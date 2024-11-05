from database_actions import DatabaseActions
from petfinder_enums import PetfinderParameters


def _same_value(pf_animal, db_animal, parameter):
    return getattr(pf_animal, parameter) == getattr(db_animal, parameter)


def determine_database_actions(pf_animals, db_animals):
    pf_ids = {pf_animals.keys()}
    db_ids = {db_animals.keys()}

    shared_ids = {id_ for id_ in pf_ids if id_ in db_ids}

    actions_by_id = {
        DatabaseActions.SHOULD_ADD: {id_ for id_ in pf_ids if id_ not in db_ids},
        DatabaseActions.MARK_REMOVED: {id_ for id_ in db_ids if id_ not in pf_ids},
        DatabaseActions.CHANGE_STATUS: {id_ for id_ in shared_ids
                                        if not _same_value(pf_animals[id_], db_animals[id_], parameter=PetfinderParameters.STATUS)},
        DatabaseActions.CHANGE_ORG_ID: {id_ for id_ in shared_ids
                                        if not _same_value(pf_animals[id_], db_animals[id_], parameter=PetfinderParameters.ORGANIZATION_ID)}
    }

    return actions_by_id
