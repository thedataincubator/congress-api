from .base import Client, SingleListParser, BaseValidator, BaseParser

class Congress:
    """Class for interacting with endpoints of the Propublica Congress API

    Parameters
    ----------
    api_key : str
        The Propublica API key to use for authentication
    """
    def __init__(self, api_key):
        self._api_key = api_key

    def get_all_members(self, congress, chamber):
        """Return a list of members of a particular chamber in a particular Congress

        Parameters
        ----------
        congress : str
            A `str` representation of an integer which denotes the desired
            meeting of congress to retrieve. I.e., the 115th congress, the
            80th congress, etc. The Propublica API supports 102-115 for
            the House and 80-115 for the Senate
        chamber : str {'house', 'senate'}

        Returns
        -------
        pandas.DataFrame
        """
        client = Client(self._api_key, 
                        SingleListParser("members"),
                        BaseValidator())
        return client.get(congress, chamber, "members.json")

    def get_member(self, member_id):
        """Return information for a particular member of Congress

        Parameters
        ----------
        member_id : str
            The ID of the member to retrieve; it is assigned by the
            Biographical Directory of the United States Congress

        Returns
        -------
        dict
            A dictionary containing the json response
        """
        client = Client(self._api_key, 
                        BaseParser(),
                        BaseValidator())
        return client.get('members', '{}.json'.format(member_id))
