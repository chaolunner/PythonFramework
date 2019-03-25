from baidu.classes.candidate import Candidate
from baidu.classes.sentiment_analysis import SentimentAnalysis
from baidu.classes.lexical_analysis import LexicalAnalysis
from json_utility import JsonUtility


@JsonUtility.register
class QueryResult:
    def __init__(self, timestamp: int = 0, status: int = 0, raw_query: str = None, candidates: [] = None,
                 qu_res_chosen: str = None, lexical_analysis: [] = None,
                 sentiment_analysis: SentimentAnalysis = None):
        self.timestamp = timestamp
        self.status = status
        self.raw_query = raw_query
        self.candidates = candidates  # type: list[Candidate]
        self.qu_res_chosen = qu_res_chosen
        self.lexical_analysis = lexical_analysis  # type: list[LexicalAnalysis]
        self.sentiment_analysis = sentiment_analysis
