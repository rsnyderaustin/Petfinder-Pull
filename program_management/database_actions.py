from enum import Enum


class DatabaseActions(Enum):
    SHOULD_ADD = 'should_add'
    CHANGE_STATUS = 'change_status'
    CHANGE_ORG_ID = 'change_org_id'
    MARK_REMOVED = 'mark_removed'
