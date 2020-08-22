import os
import requests
from jose import jwt
from cachetools import TTLCache

class Security:

    def __init__(self):
        self.cache = TTLCache(maxsize=10, ttl=22189)

    def verify_token(self, token):
        audience = os.environ['project_id']
        issuer = 'https://accounts.google.com'
        jwt.decode(token, self.prepare_jwks(), algorithms=[
                   'RS256'], audience=audience, issuer=issuer)

    def prepare_jwks(self):
        try:
            return self.cache['jwks']
        except:
            self.cache['jwks'] = requests.get(
                'https://www.googleapis.com/oauth2/v3/certs').content
            return self.cache['jwks']
