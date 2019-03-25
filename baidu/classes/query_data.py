from baidu.classes.dialog_state import DialogState
from baidu.classes.query_request import QueryRequest
from json_utility import JsonUtility


@JsonUtility.register
class QueryData:
    def __init__(self, version: str = None, service_id: str = None, skill_ids: [] = None, log_id: str = None,
                 session_id: str = None, dialog_state: DialogState = None, request: QueryRequest = None):
        self.version = version
        self.service_id = service_id
        self.skill_ids = skill_ids
        self.log_id = log_id
        self.session_id = session_id
        self.dialog_state = dialog_state
        self.request = request
