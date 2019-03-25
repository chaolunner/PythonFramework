from json_utility import JsonUtility


@JsonUtility.register
class Slots:
    def __init__(self, confidence: float = 0, begin: int = 0, length: int = 0, original_word: str = None,
                 normalized_word: str = None, word_type: str = None, name: str = None, session_offset: int = 0,
                 merge_method: str = None, sub_slots: [] = None, need_clarify: bool = False, father_idx: int = 0):
        self.confidence = confidence
        self.begin = begin
        self.length = length
        self.original_word = original_word
        self.normalized_word = normalized_word
        self.word_type = word_type
        self.name = name
        self.session_offset = session_offset
        self.merge_method = merge_method
        self.sub_slots = sub_slots  # type:list[Slots]
        self.need_clarify = need_clarify
        self.father_idx = father_idx
