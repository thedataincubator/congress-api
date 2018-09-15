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

@responses.activate
def test_all_members_getter(congress, client):
    congress_no = '115'
    chamber = 'senate'
    # Read json sample.
    json_sample_name = 'test/api_output_samples/all_members_sample.json'
    assert os.path.exists(json_sample_name)
    with open(json_sample_name) as json_sample:
        mock_json = json.load(json_sample)
    # Mock API response.
    api_url = client.build_url(congress_no, chamber, "members.json")
    responses.add(responses.GET, api_url, json=mock_json, status=200)
    # Test get_all_members().
    all_members_df = congress.get_all_members(congress_no, chamber)
    assert len(all_members_df.index) == 104

@responses.activate
def test_member_getter(congress, client):
    member_id = 'K000388'
    # Read json sample.
    json_sample_name = 'test/api_output_samples/member_sample.json'
    assert os.path.exists(json_sample_name)
    with open(json_sample_name) as json_sample:
        mock_json = json.load(json_sample)
    # Mock API response.
    api_url = client.build_url('members', '{}.json'.format(member_id))
    responses.add(responses.GET, api_url, json=mock_json, status=200)
    # Test get_member().
    member_output = congress.get_member(member_id)
    assert member_output == mock_json
