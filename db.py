from flask import jsonify
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
        return self._user.insert_one({"mail": mail, "pwd": password})

    def get_user(self, mail):
        return self._user.find_one({"mail": mail})

    def mail_already_exist(self, mail):
        return self._user.find_one({"mail": mail})

    # CITATIONS

    def get_all_citations(self):
        return list(self._citation.find({}))

    def add_citation(self, citation, author,oeuvre,date,langue):
        self._citation.insert_one({"text": citation, "author": author,"oeuvre":oeuvre,"date":date,"langue":langue})