import pytest
import responses
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
    # Init testing values.
    congress_no = '114'
    chamber = 'senate'
    n_members = 100
    # Mock API response.
    api_url = client.build_url(congress_no, chamber, "members.json")
    mock_members = [dict()] * n_members
    mock_results = [{'members': mock_members}]
    mock_json = {'status': 'OK', 'results': mock_results}
    responses.add(responses.GET, api_url, json=mock_json, status=200)
    # Test get_all_members().
    all_members_df = congress.get_all_members(congress_no, chamber)
    assert len(all_members_df.index) == n_members

@responses.activate
def test_member_getter(congress, client):
    # Init testing value.
    member_id = 'A000360'
    # Mock API response.
    api_url = client.build_url('members', '{}.json'.format(member_id))
    mock_results = [{'member_id': member_id}]
    mock_json = {'status': 'OK', 'results': mock_results}
    responses.add(responses.GET, api_url, json=mock_json, status=200)
    # Test get_member().
    member_results = congress.get_member(member_id)['results']
    assert len(member_results) == 1
    assert member_results[0]['member_id'] == member_id
