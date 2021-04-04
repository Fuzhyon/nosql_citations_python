from pymongo import MongoClient


class MongoDBConnector:

    def __init__(self):
        self._client = MongoClient('localhost:27017')
        self._db = self._client.citations_db
        self._user = self._db.user
        self._citation = self._db.citation

    # USERS

    def get_all_user(self):
        return list(self._db.user.find({}))

    def add_user(self, mail, password):
        self._user.insert_one({"mail": mail, "pwd": password})

    def get_user(self):
        return self._user.find_one()

    # CITATIONS

    def get_all_citations(self):
        return list(self._user.find({}))
