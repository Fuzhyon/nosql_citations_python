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
        return self._user.insert_one({"mail": mail, "pwd": password,"favorite":[]})

    def get_user(self, mail):
        return self._user.find_one({"mail": mail})

    def mail_already_exist(self, mail):
        return self._user.find_one({"mail": mail})

    # CITATIONS

    def get_all_citations(self):
        return list(self._citation.find({}))

    def add_citation(self, citation, author, oeuvre, date, langue, user):
        return self._citation.insert_one(
            {"text": citation, "author": author, "oeuvre": oeuvre, "date": date, "langue": langue, "user": user})
    def get_citation(self, citation):
        return self._citation.find_one({"mail": citation})
    def delete_citation(self,citation):
        response = self._citation.delete_one({"text": citation})
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
