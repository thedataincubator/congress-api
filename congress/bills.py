from .base import Client, SingleListParser, BaseValidator, BaseParser

class Bills:
    def __init__(self, api_key):
        self._api_key = api_key

    def search_bills(self, query):
        client = Client(self._api_key, 
                        SingleListParser("bills"),
                        BaseValidator())
        return client.get('bills/search.json?query={}'.format(query))        
        
    def get_recent_bills(self, congress, chamber, bill_type):
        client = Client(self._api_key, 
                        SingleListParser("bills"),
                        BaseValidator())
        return client.get(congress, chamber, 'bills/{}.json".format(bill_type))

    def get_upcoming_bills(self, chamber):
        client = Client(self._api_key, 
                        SingleListParser("bills"),
                        BaseValidator())
        return client.get('bills', 'upcoming', '{}.json'.format(chamber))
    
    def get_amendments(self, congress, bill_id):
        client = Client(self._api_key, 
                        SingleListParser("amendments"),
                        BaseValidator())
        return client.get(congress, 'bills', bill_id, 'amendments.json')

    def get_subjects(self, congress, bill_id):
        client = Client(self._api_key, 
                        SingleListParser("subjects"),
                        BaseValidator())
        return client.get(congress, 'bills', bill_id, 'subjects.json')

    def get_related_bills(self, congress, bill_id):
        client = Client(self._api_key, 
                        SingleListParser("related_bills"),
                        BaseValidator())
        return client.get(congress, 'bills', bill_id, 'related.json')

    def search_subjects(self, query):
        client = Client(self._api_key, 
                        SingleListParser("subjects"),
                        BaseValidator())
        return client.get('bills/subjects/search.json?query={}'.format(query))

    def get_cosponsors(self, congress, bill_id):
        # does not include sponsor
        client = Client(self._api_key, 
                        SingleListParser("cosponsors"),
                        BaseValidator())
        return client.get(congress, 'bills', bill_id, 'cosponsors.json')
