import time

try:
    from urllib.request import urlopen, Request  # Python 3
except ImportError:
    from urllib2 import urlopen, Request  # Python 2

from baidu.classes.access_token import AccessToken
from baidu.classes.query_data import QueryData
from baidu.classes.query_request import QueryRequest
from baidu.classes.dialog_state import DialogState
from baidu.classes.response_data import ResponseData
from json_utility import JsonUtility
from os_utility import OSUtility
from aip import AipSpeech


class BaiduUtility:
    app_id = "15554198"
    api_key = "K42tgyWzgAkPSC9gVaYWkeg7"
    secret_key = "TlBoDLWCMZmjE9P6VFRUz2e24NKh1Vv7"
    access_token = None  # type: str
    aip_speech = None  # type:AipSpeech
    response_dict = {}  # type: dict[str, ResponseData]
    # 3: mp3 4: pcm-16k 5: pcm-8k 6: wav
    synthesis_formats = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
    synthesis_aue = 4
    synthesis_format = synthesis_formats[synthesis_aue]

    # Request to authorization service 'https://aip.baidubce.com/oauth/2.0/token' and add the following parameters to the URL
    # grant_type=client_credentials
    # client_id=Your app API Key
    # client_secret=Your app Secret Key
    @staticmethod
    def get_access_token():
        if BaiduUtility.access_token is not None:
            return BaiduUtility.access_token

        host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}&".format(
            BaiduUtility.api_key, BaiduUtility.secret_key)
        request = Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        f = urlopen(request)
        content = f.read()
        try:
            msg = JsonUtility.from_json(content)  # type: AccessToken
            BaiduUtility.access_token = msg.access_token
            return BaiduUtility.access_token
        except ValueError:
            return None

    @staticmethod
    def request_query(query: str, log_id: str = None, version: float = 2.0, service_id: str = "S13677",
                      skill_ids: [] = None, session_id: str = None, user_id: str = "dev") -> ResponseData:
        if BaiduUtility.response_dict.__contains__(query):
            return BaiduUtility.response_dict.get(query)

        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + BaiduUtility.get_access_token()
        query_data = QueryData()
        if log_id is None:
            query_data.log_id = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            query_data.log_id = log_id
        query_data.version = version
        query_data.service_id = service_id
        if skill_ids is None:
            skill_ids = ["36984"]
        query_data.skill_ids = skill_ids
        if session_id is None:
            query_data.session_id = ""
        else:
            query_data.session_id = session_id
        query_data.request = QueryRequest()
        query_data.request.query = query
        query_data.request.user_id = user_id
        query_data.dialog_state = DialogState()
        query_data.dialog_state.contexts = {"SYS_REMEMBERED_SKILLS": skill_ids}
        post_data = JsonUtility.to_json(query_data).encode(encoding="utf-8")
        request = Request(url, post_data)
        request.add_header('Content-Type', 'application/json')
        content = urlopen(request)
        response_data = JsonUtility.from_json(content.read())
        BaiduUtility.response_dict.__setitem__(query, response_data)
        return response_data

    @staticmethod
    def get_aip_speech():
        if BaiduUtility.aip_speech is None:
            BaiduUtility.aip_speech = AipSpeech(BaiduUtility.app_id, BaiduUtility.api_key, BaiduUtility.secret_key)
        return BaiduUtility.aip_speech

    @staticmethod
    def synthesis(tex: str, lang: str = 'zh', ctp: int = 1, overwrite: bool = False,
                  options: dict = None):

        path = "resources\\audios\\{0}.{1}".format(tex, BaiduUtility.synthesis_format)
        if overwrite is False and OSUtility.exists(path):
            return OSUtility.open(path)

        if options is None:
            options = {'aue': BaiduUtility.synthesis_aue}
        else:
            options.__setitem__('aue', BaiduUtility.synthesis_aue)

        synthesis_result = BaiduUtility.get_aip_speech().synthesis(tex, lang, ctp, options)

        if not isinstance(synthesis_result, dict):
            OSUtility.create(path, synthesis_result)
            return OSUtility.open(path)
        else:
            raise ValueError(synthesis_result.get('err_msg'))

    @staticmethod
    def asr(speech: [], asr_format: str = 'pcm', rate: int = 16000, options: dict = None) -> [str]:
        asr_result = BaiduUtility.get_aip_speech().asr(speech, asr_format, rate, options)
        if asr_result.get('err_no') == 0:
            return asr_result.get('result')
        else:
            raise ValueError(
                "error_code: {0}, error_msg: {1}".format(asr_result.get('err_no'), asr_result.get('err_msg')))

    @staticmethod
    def clear():
        """
        Delete all saved audio files
        """
        OSUtility.removedirs("resources\\audios")


if __name__ == '__main__':
    data = BaiduUtility.request_query("往前走10米")
    if data.error_code == 0:
        for response in data.result.response_list:
            print("intent: {0}".format(response.schema.intent))
            for slot in response.schema.slots:
                print("name: {0}, normalized word : {1}".format(slot.name, slot.normalized_word))
    else:
        raise ValueError(data.error_msg)

    for result in BaiduUtility.asr(BaiduUtility.synthesis("嘿小派"), options={'dev_pid': 1536}):
        print(result)
