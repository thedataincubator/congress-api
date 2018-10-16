from .base import Client, SingleListParser, BaseValidator, BaseParser


class Votes:
    """Class for interacting with `Votes` endpoint of the Propublica Congress API

    Parameters
    ----------
    api_key : str
        The Propublica API key to use for authentication
    """

    def __init__(self, api_key):
        self._api_key = api_key

    def get_recent_votes(self, chamber, offset=0):
        """Return the 20 most recent results, sorted by date and roll call number

        Parameters
        ----------
        chamber : str
            `house`, `senate`, `both`
        offset : int
            This value offsets the returns of recent results

        Returns
        -------
        dict
            A dictionary containing the json response
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(chamber, "votes/recent.json", offset=offset)

    def get_rollcall_votes(self, congress, chamber, ses_no, rcall_no):
        """
        Return roll call votes

        Parameters
        ----------
        congress : str
            From 102 to 115 for House, and from 80 to 115 for Senate
        chamber : str
            `house`, `senate`
        ses_no : str
            Session number: `1` or `2`, depending on year
            `1` is odd-numbered years, `2` is even-numbered years
        rcall_no : str
            Roll call number

        Returns
        -------
        dict
            A dictionary containing the json response

        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(congress, chamber,
                          "sessions", ses_no, "votes",
                          "{}.json".format(rcall_no))

    def get_votesbytype(self, congress, chamber, vote_type):
        """
        Return votes by type

        Parameters
        ----------
        congress : str
            From 102 to 115 for House, and from 80 to 115 for Senate
        chamber : str
            `house`, `senate`
        vote_type : str
            `missed`, `party`, `loneno` or `perfect`

        Returns
        -------
        pandas.DataFrame
        """
        if vote_type not in ['missed', 'party', 'loneno', 'perfect']:
            raise ValueError('vote_type can only be one of '
                             '[missed,party,loneno,perfect]')

        client = Client(self._api_key,
                        SingleListParser("members"),
                        BaseValidator())
        return client.get(congress, chamber,
                          "votes", "{}.json".format(vote_type))

    def get_votesbydate(self, chamber, year, month):
        """
        Return all votes for one or both chambers in a particular month

        Parameters
        ----------
        chamber : str
            `house`, `senate`, `both`
        year : str
            YYYY format
        month : str
            MM format

        Returns
        -------
        dict
            A dictionary containing the json response
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(chamber, "votes",
                          year, "{}.json".format(month))

    def get_nomination_votes(self, congress):
        """
        Return Senate votes on presidential nominations

        Parameters
        ----------
        congress : str
            From 101 to 115

        Returns
        -------
        dict
            A dictionary containing the json response
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(congress, "nominations.json")

    def recent_expl(self, congress, offset=0):
        """
        Return personal explanations for missed or mistaken votes.

        Parameters
        ----------
        congress : str
            From 107 to 115
        offset : int
            This value offsets the returns of recent results

        Returns
        -------
        dict
            A dictionary containing the json response
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(congress, "explanations.json", offset=offset)

    def recent_expl_votes(self, congress, offset=0):
        """
        Return explanations parsed to individual votes and reason.
        Parameters
        ----------
        congress : str
            From 110 to 115
        offset : int
            This value offsets the returns of recent results.

        Returns
        -------
        dict
            A dictionary containing the json response.
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(congress, "explanations",
                          "votes.json", offset=offset)

    def recent_expl_bycat(self, congress, category, offset=0):
        """
        Return personal explanations for missed or mistaken votes.

        Parameters
        ----------
        congress : str
            From 110 to 115
        category : str
            "voted-incorrectly","official-business","personal"
            See all parameters at
            https://projects.propublica.org/api-docs/congress-api/votes/#get-recent-personal-explanation-votes-by-category
        offset : int
            This value offsets the returns of recent results.

        Returns
        -------
        dict
            A dictionary containing the json response.
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get(congress, "explanations", "votes",
                          "{}.json".format(category), offset=offset)

    def recent_expl_byper(self, member_id, congress, offset=0):
        """
        Return recent personal explanations by a specific member.

        Parameters
        ----------
        congress : str
            From 110 to 115
        member_id : str
            This can be retrieved from a member list request.
        offset : int
            This value offsets the returns of recent results

        Returns
        -------
        dict
            A dictionary containing the json response.
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get("members", member_id, "explanations",
                          "{}.json".format(congress), offset=offset)

    def recent_expl_votes_byper(self, member_id, congress, offset=0):
        """
        Return recent personal explanations for missed or mistaken votes.

        Parameters
        ----------
        congress : str
            From 110 to 115
        member_id : str
            This can be retrieved from a member list request.
        offset : int
            This value offsets the returns of recent results

        Returns
        -------
        dict
            A dictionary containing the json response
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get("members", member_id, "explanations",
                          congress, "votes.json", offset=offset)

    def recent_expl_bycat_byper(self, congress, category, member_id, offset=0):
        """
        Return personal explanations for missed or mistaken votes.

        Parameters
        ----------
        congress : str
            From 110 to 115
        category : str
            "voted-incorrectly","official-business","personal"
            See all parameters at
            https://projects.propublica.org/api-docs/congress-api/votes/#get-recent-personal-explanation-votes-by-category
        member_id : str
            This can be retrieved from a member list request.
        offset : int
            This value offsets the returns of recent results.

        Returns
        -------
        dict
            A dictionary containing the json response.
        """

        client = Client(self._api_key,
                        BaseParser(),
                        BaseValidator())
        return client.get("members", member_id, "explanations",
                          congress, "votes",
                          "{}.json".format(category), offset=offset)
