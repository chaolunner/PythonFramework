from json_utility import JsonUtility


@JsonUtility.register
class AccessToken:
    def __init__(self, refresh_token: str = None, expires_in=0, scope: str = None, session_key: str = None,
                 access_token: str = None, session_secret: str = None):
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.scope = scope
        self.session_key = session_key
        self.access_token = access_token
        self.session_secret = session_secret
