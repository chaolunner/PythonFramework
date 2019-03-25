from baidu.classes.slots import Slots
from json_utility import JsonUtility


@JsonUtility.register
class Schema:
    def __init__(self, intent_confidence: float = 0, slots: [] = None, domain_confidence: float = 0,
                 intent: str = None):
        self.intent_confidence = intent_confidence
        self.slots = slots  # type:list[Slots]
        self.domain_confidence = domain_confidence
        self.intent = intent
