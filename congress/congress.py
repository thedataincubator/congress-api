from .base import Client, SingleListParser, BaseValidator, BaseParser

class Congress:
    def __init__(self, api_key):
        self._api_key = api_key

    def get_all_members(self, congress, chamber):
        client = Client(self._api_key, 
                        SingleListParser("members"),
                        BaseValidator())
        return client.get(congress, chamber, "members.json")

    def get_member(self, member_id):
        client = Client(self._api_key, 
                        BaseParser(),
                        BaseValidator())
        return client.get('members', '{}.json'.format(member_id))
