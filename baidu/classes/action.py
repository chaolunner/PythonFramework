from baidu.classes.refine_detail import RefineDetail
from json_utility import JsonUtility


@JsonUtility.register
class Action:
    def __init__(self, action_id: str = None, refine_detail: RefineDetail = None, confidence: float = 0,
                 custom_reply: str = None, say: str = None, type: str = None):
        self.action_id = action_id
        self.refine_detail = refine_detail
        self.confidence = confidence
        self.custom_reply = custom_reply
        self.say = say
        self.type = type
