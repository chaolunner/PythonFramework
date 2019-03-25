from json_utility import JsonUtility


@JsonUtility.register
class DialogState:
    def __init__(self, skill_states: dict = None, contexts: dict = None):
        self.skill_states = skill_states
        self.contexts = contexts
