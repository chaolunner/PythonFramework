from baidu.classes.action import Action
from baidu.classes.schema import Schema
from baidu.classes.query_result import QueryResult
from json_utility import JsonUtility


@JsonUtility.register
class Response:
    def __init__(self, status: int = 0, msg: str = None, origin: str = None, action_list: [] = None,
                 schema: Schema = None, qu_res: QueryResult = None):
        self.status = status
        self.msg = msg
        self.origin = origin
        self.action_list = action_list  # type: list[Action]
        self.schema = schema
        self.qu_res = qu_res
