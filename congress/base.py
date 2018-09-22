import json
import pandas as pd
import requests
from urllib.parse import urljoin
from .errors import CongressError

BASE_URL = 'https://api.propublica.org/congress/{version}'

class Client:
    """A client for making requests to the API

    Parameters
    ----------
    api_key : str
        An API key for authentication
    parser : parser object
        An object which implements a `parse` method that is capable of
        handling a json object
    validator : validator object
    version : str
        The version of the api to access. Defaults to 'v1'.
    """

    def __init__(self, api_key, parser, validator, version='v1'):
        self._api_key = api_key
        self._version = version
        self._parse = parser.parse
        self._validate = validator.validate

    def _headers(self):
        """Assemble the proper header with the API key

        Returns
        -------
        dict
            A dictionary of headers for an http request
        """
        return {
            'X-API-KEY': self._api_key
        }

    def _response(self, resp):
        """Check the API response and load json as a string

        Parameters
        ----------
        resp : requests.Response

        Returns
        -------
        self._parse(json_)
            Returns the output of `self._parse`, which is the `parse`
            method for whichever parser the `Client` was instantiated with

        Raises
        ------
        CongressError
            If the http `resp.status` is not "200" or if the
            `json` object's `status` attribute is not "OK"
        """
        if not resp.ok:
            raise CongressError
        json_ = json.loads(resp.text)
        if not json_.get('status') == "OK":
            raise CongressError
        return self._parse(json_)
        
    def build_url(self, *args):
        """Construct the proper URL from a list of arguments

        Parameters
        ----------
        *args : Arguments

        Returns
        -------
        url : str
            The URL to be used in the API request
        """
        url = BASE_URL.format(version=self._version)
        for arg in args:
            url = urljoin(url + '/', arg)
        return url

    def get(self, *args, **kwargs):
        """Make a GET request from the API

        Parameters
        ----------
        *args : Arguments
        **kwargs : Keyword Arguments
            A data payload to send in the body of the http request.
            For instance, calling with
            `get('endpoint', **{'key1':'val1', 'key2':'val2'})`
            will send a request of the form
            `https://api.propublica.org/congress/v1/endpoint?key1=val1&key2=val2`.
            See `Passing Parameters In URLs <http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls>`_

        Returns
        -------
            Returns the output of whatever parser object the `Client` was
            instantiated with

        """
        self._validate(*args, **kwargs)
        r = requests.get(self.build_url(*args), 
                         params=kwargs,
                         headers=self._headers())

        return self._response(r)

class BaseValidator:
    """ Base class for all validator types
    """

    def validate(self, *args, **kwargs):
        """
        Parameters
        ----------
        *args : Arguments
        **kwargs : Keyword Arguments
        """
        pass

class BaseParser:
    """ Base class for all parser types
    """
    def parse(self, json_):
        return json_

class SingleListParser(BaseParser):
    """Parse a json payload and turn it into a pandas DataFrame

    Parameters
    ----------
    key: str
        The key of the json object to return
    """

    def __init__(self, key):
        super().__init__()
        self.key = key

    def parse(self, json_):
        """Parse a json payload and turn it into a pandas DataFrame

        Parameters
        ----------
        json_ : str
            A json result to be parsed

        Returns
        -------
        pandas.DataFrame
        """
        return pd.DataFrame(
            json_['results'][0][self.key]
        )
