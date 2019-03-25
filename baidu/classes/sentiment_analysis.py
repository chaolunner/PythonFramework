from json_utility import JsonUtility


@JsonUtility.register
class SentimentAnalysis:
    def __init__(self, label: str = None, pval: float = 0):
        self.label = label
        self.pval = pval
