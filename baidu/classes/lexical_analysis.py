from json_utility import JsonUtility


@JsonUtility.register
class LexicalAnalysis:
    def __init__(self, term: str = None, weight: float = 0, type: str = None, etypes: [] = None, basic_word: [] = None):
        self.term = term
        self.weight = weight
        self.type = type
        self.etypes = etypes
        self.basic_word = basic_word
