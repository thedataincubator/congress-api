import pytest
from congress import Congress

@pytest.fixture
def congress():
    api_key = 'testing_key'
    return Congress(api_key)

def test_all_members_getter(congress):
    congress_no = '114'
    chamber = 'senate'
    all_members_df = congress.get_all_members(congress_no, chamber)
    assert len(all_members_df.index) == 100

def test_member_getter(congress):
    member_id = 'A000360'
    member_results = congress.get_member(member_id)['results']
    assert len(member_results) == 1
    assert member_results[0]['member_id'] == member_id
