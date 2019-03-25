from baidu.classes.dialog_state import DialogState
from baidu.classes.response import Response
from json_utility import JsonUtility


@JsonUtility.register
class ResponseResult:
    def __init__(self, version: str = None, service_id: str = None, log_id: str = None, session_id: str = None,
                 dialog_state: DialogState = None, interaction_id: str = None, timestamp: str = None,
                 response_list: [] = None):
        self.version = version
        self.service_id = service_id
        self.log_id = log_id
        self.session_id = session_id
        self.dialog_state = dialog_state
        self.interaction_id = interaction_id
        self.timestamp = timestamp
        self.response_list = response_list  # type:list[Response]
