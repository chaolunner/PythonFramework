from baidu.classes.response_result import ResponseResult
from json_utility import JsonUtility


@JsonUtility.register
class ResponseData:
    def __init__(self, error_code: int = 0, error_msg: str = None, result: ResponseResult = None):
        self.error_code = error_code
        self.error_msg = error_msg
        self.result = result
