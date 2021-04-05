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
        return self._user.insert_one({"mail": mail, "pwd": password, "favorite": []})

    def get_user(self, mail):
        return self._user.find_one({"mail": mail})

    def user_add_favorite(self, mail, id):
        user = self.get_user(mail)
        user['favorite'].append(id)
        return self._user.update({"mail": mail}, user)

    def user_remove_favorite(self, mail, id):
        user = self.get_user(mail)
        user['favorite'].remove(id)
        return self._user.update({"mail": mail}, user)


    def mail_already_exist(self, mail):
        return self._user.find_one({"mail": mail})

    # CITATIONS

    def get_all_citations(self):
        return list(self._citation.find({}))

    def add_citation(self, citation, author, oeuvre, date, langue, user):
        return self._citation.insert_one(
            {"text": citation, "author": author, "oeuvre": oeuvre, "date": date, "langue": langue, "added_by": user})

    def get_citation(self, id_citation):
        return self._citation.find_one({"_id": id_citation})

    def delete_citation(self, id_citation):
        return self._citation.delete_one({"_id": id_citation})
