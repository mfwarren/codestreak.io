import requests
import time
import os
import json

EXPIRES_IN = 86400

auth_id = os.environ['AUTH0_CLIENT_ID']
auth_secret = os.environ['AUTH0_CLIENT_SECRET']
auth_callback_url = os.environ['AUTH0_CALLBACK_URL']
auth_domain = os.environ['AUTH0_DOMAIN']


class Auth0Token(object):
    """the JWT tokens expire after a while. this caches it until the time is up then
    will request a new token"""

    def __init__(self):
        super().__init__()
        self._token = None
        self._expires_at = 0

    def is_expired(self):
        return time.time() >= self._expires_at

    def get_token(self):
        if not self.is_expired and self._token:
            return self._token

        json_header = {'content-type': 'application/json'}

        token_url = 'https://{0}/oauth/token'.format(auth_domain)
        token_payload = {
            'client_id': auth_id,
            'client_secret': auth_secret,
            'audience': 'https://halotis.auth0.com/api/v2/',
            'grant_type': 'client_credentials'
        }

        # Fetch new JWT
        token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()

        self._token = token_info['access_token']
        self._expires_at = time.time() + EXPIRES_IN