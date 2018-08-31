import json
import pandas as pd
import requests
from urllib.parse import urljoin
from .errors import CongressError

BASE_URL = 'https://api.propublica.org/congress/{version}'

class Client:

    def __init__(self, api_key, parser, validator, version='v1'):
        self._api_key = api_key
        self._version = version
        self._parse = parser.parse
        self._validate = validator.validate

    def _headers(self):
        return {
            'X-API-KEY': self._api_key
        }

    def _response(self, resp):
        if not resp.ok:
            raise CongressError
        json_ = json.loads(resp.text)
        if not json_.get('status') == "OK":
            raise CongressError
        return self._parse(json_)
        
    def build_url(self, *args):
        url = BASE_URL.format(version=self._version)
        for arg in args:
            url = urljoin(url + '/', arg)
        return url

    def get(self, *args, **kwargs):
        self._validate(*args, **kwargs)
        r = requests.get(self.build_url(*args), 
                         params=kwargs,
                         headers=self._headers())

        return self._response(r)

class BaseValidator:

    def validate(self, *args, **kwargs):
        pass

class BaseParser:
    
    def parse(self, json_):
        return json_

class SingleListParser(BaseParser):

    def __init__(self, key):
        super().__init__()
        self.key = key

    def parse(self, json_):
        return pd.DataFrame(
            json_['results'][0][self.key]
        )
