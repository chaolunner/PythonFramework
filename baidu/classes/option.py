from json_utility import JsonUtility


@JsonUtility.register
class Option:
    def __init__(self, option: str = None, info: dict = None):
        self.option = option
        self.info = info
