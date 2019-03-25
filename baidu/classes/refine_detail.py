from baidu.classes.option import Option
from json_utility import JsonUtility


@JsonUtility.register
class RefineDetail:
    def __init__(self, option_list: [] = None, interact: str = None, clarify_reason: str = None):
        self.option_list = option_list  # type: list[Option]
        self.interact = interact
        self.clarify_reason = clarify_reason
