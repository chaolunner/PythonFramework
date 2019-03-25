from json_utility import JsonUtility


@JsonUtility.register
class QueryRequest:
    def __init__(self, user_id: str = None, query: str = None, client_session: str = None):
        self.user_id = user_id
        self.query = query
        self.client_session = client_session
