import pytest
import responses
import os
import json
from congress import Votes, Client, BaseParser, BaseValidator

@pytest.fixture
def votes():
    api_key = 'testing_key'
    return Votes(api_key)

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
def test_get_recent_votes(votes, client, read_json):
    chamber = 'house'
    # Read json sample.
    json_sample_name = 'test/api_response_samples/all_members_sample.json'
    mock_json = read_json(json_sample_name)
    # Mock API response.
    api_url = client.build_url(chamber,"votes/recent.json?offset=0")
    print(api_url)
    responses.add(responses.GET, api_url, json=mock_json, \
                    status=200,match_querystring=True)
    # Test get_all_members().
    recent_votes_dict = votes.get_recent_votes(chamber)
    assert recent_votes_dict == mock_json

@responses.activate
def test_get_rollcall_votes(votes,client,read_json):
    congress_no='115'
    chamber = 'senate'
    session_no = '1'
    roll_call_no='17'

    json_sample_name = 'test/api_response_samples/get_rollcall_votes.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(congress_no,chamber,\
                          "sessions",session_no,"votes",\
                          roll_call_no+".json")
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    rocall_votes = votes.get_rollcall_votes(congress_no,chamber,session_no,roll_call_no)
    assert rocall_votes == mock_json


@responses.activate
def test_get_votesbytype(votes,client,read_json):
    congress_no='105'
    chamber = 'senate'
    vote_type = 'party'

    json_sample_name = 'test/api_response_samples/get_votesbytype.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(congress_no,chamber,"votes",\
                          vote_type+".json") 
    print(api_url)
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    votesbytype_df = votes.get_votesbytype(congress_no,chamber,vote_type)
    assert votesbytype_df.shape == (100,10)

@responses.activate
def test_get_votesbydate(votes,client,read_json):
    chamber = 'senate'
    year = '2016'
    month = '04'
    
    json_sample_name = 'test/api_response_samples/get_votesbydate.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(chamber,"votes",\
                          year,month+".json")
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    votesbydate = votes.get_votesbydate(chamber,year,month)
    assert votesbydate == mock_json

@responses.activate
def test_get_nomination_votes(votes,client,read_json):
    congress_no = '110'

    json_sample_name = 'test/api_response_samples/get_nomination_votes.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(congress_no,"nominations.json")
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    nomination_votes = votes.get_nomination_votes(congress_no)
    assert nomination_votes == mock_json

@responses.activate
def test_recent_expl(votes,client,read_json):
    congress_no = '114'

    json_sample_name = 'test/api_response_samples/recent_expl.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(congress_no,"explanations.json?offset=0")
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    explanation = votes.recent_expl(congress_no)
    assert explanation == mock_json

@responses.activate
def test_recent_expl_votes(votes,client,read_json):
    congress_no = '114'

    json_sample_name = 'test/api_response_samples/recent_expl_votes.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(congress_no,"explanations",\
                          "votes.json?offset=0")
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    explanation = votes.recent_expl_votes(congress_no)
    assert explanation == mock_json

@responses.activate
def test_recent_expl_bycat(votes,client,read_json):
    congress_no = '115'
    category = 'voted-incorrectly'

    json_sample_name = 'test/api_response_samples/recent_expl_bycat.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url(congress_no,"explanations","votes",\
                          category+".json?offset=0")
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    explanation = votes.recent_expl_bycat(congress_no,category)
    assert explanation == mock_json

@responses.activate
def test_recent_expl_votes_byper(votes,client,read_json):
    congress_no = '115'
    member_id = 'S001193' 

    json_sample_name = 'test/api_response_samples/recent_expl_votes_byper.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url("members",member_id,"explanations",\
                          congress_no,"votes.json?offset=0")
    
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    explanation = votes.recent_expl_votes_byper(member_id,congress_no)
    assert explanation == mock_json

@responses.activate
def test_recent_expl_bycat_byper(votes,client,read_json):
    congress_no = '115'
    category = 'personal'
    member_id = 'S001193' 

    json_sample_name = 'test/api_response_samples/recent_expl_bycat_byper.json'
    mock_json = read_json(json_sample_name)
    
    api_url=client.build_url("members",member_id,"explanations",\
                          congress_no,"votes",\
                          category+".json?offset=0")
    print(api_url)
    responses.add(responses.GET,api_url,json=mock_json,status=200)
    explanation = votes.recent_expl_bycat_byper(congress_no,category,member_id)
    assert explanation == mock_json





