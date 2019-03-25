from baidu.classes.slots import Slots
from json_utility import JsonUtility


@JsonUtility.register
class Candidate:
    def __init__(self, confidence: float = 0, intent: str = None, intent_confidence: float = 0,
                 intent_need_clarify: bool = False, slots: [] = None, from_who: str = None, match_info: str = None,
                 extra_info: dict = None):
        self.confidence = confidence
        self.intent = intent
        self.intent_confidence = intent_confidence
        self.intent_need_clarify = intent_need_clarify
        self.slots = slots  # type: list[Slots]
        self.from_who = from_who
        self.match_info = match_info
        self.extra_info = extra_info
