import pytest
import responses
from congress import Client, BaseParser, BaseValidator
from congress import CongressError, APIError

@pytest.fixture
def client():
    api_key = 'testing_key'
    return Client(api_key, BaseParser(), BaseValidator())

def test_url_builder(client):
    assert client.build_url() == 'https://api.propublica.org/congress/v1'
    assert client.build_url('route') == 'https://api.propublica.org/congress/v1/route'
    assert client.build_url('route', 'another') == 'https://api.propublica.org/congress/v1/route/another'

@responses.activate
def test_bad_response(client):
    responses.add(
        responses.GET,
        'https://api.propublica.org/congress/v1',
        status=404
    )
    with pytest.raises(APIError):
        client.get()

