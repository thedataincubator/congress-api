import pytest
import responses
import os
import json
from congress import Congress, Client, BaseParser, BaseValidator

@pytest.fixture
def congress():
    api_key = 'testing_key'
    return Congress(api_key)

@pytest.fixture
def client():
    api_key = 'testing_key'
    return Client(api_key, BaseParser(), BaseValidator())

@pytest.fixture
def read_json():
    def json_reader(json_name):
        with open(json_name) as json_file:
            json_data = json.load(json_file)
        return json_data

    return json_reader

@responses.activate
def test_all_members_getter(congress, client, read_json):
    congress_no = '115'
    chamber = 'senate'
    # Read json sample.
    json_sample_name = 'test/api_response_samples/all_members_sample.json'
    mock_json = read_json(json_sample_name)
    # Mock API response.
    api_url = client.build_url(congress_no, chamber, "members.json")
    responses.add(responses.GET, api_url, json=mock_json, status=200)
    # Test get_all_members().
    all_members_df = congress.get_all_members(congress_no, chamber)
    assert all_members_df.shape == (104, 44)

@responses.activate
def test_member_getter(congress, client, read_json):
    member_id = 'K000388'
    # Read json sample.
    json_sample_name = 'test/api_response_samples/member_sample.json'
    mock_json = read_json(json_sample_name)
    # Mock API response.
    api_url = client.build_url('members', '{}.json'.format(member_id))
    responses.add(responses.GET, api_url, json=mock_json, status=200)
    # Test get_member().
    get_member_response = congress.get_member(member_id)
    assert get_member_response == mock_json
