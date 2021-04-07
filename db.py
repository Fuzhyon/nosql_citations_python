from bson import ObjectId
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
        return self._user.insert_one({"mail": mail, "pwd": password, "favorite": [], "mes_ajouts": []})

    def get_user(self, mail):
        return self._user.find_one({"mail": mail})

    def user_add_favorite(self, mail, id_citation):
        user = self.get_user(mail)
        user['favorite'].append(id_citation)
        return self._user.update({"mail": mail}, user)

    def user_remove_favorite(self, mail, id_citation):
        user = self.get_user(mail)
        user['favorite'].remove(id_citation)
        return self._user.update({"mail": mail}, user)

    def user_add_mes_ajouts(self, mail, id_citation):
        user = self.get_user(mail)
        if user:
            user['mes_ajouts'].append(id_citation)
        return self._user.update({"mail": mail}, user)

    def user_remove_mes_ajouts(self, mail, id_citation):
        user = self.get_user(mail)
        if user:
            if id_citation in user['mes_ajouts']:
                user['mes_ajouts'].remove(id_citation)

        return self._user.update({"mail": mail}, user)

    def mail_already_exist(self, mail):
        return self._user.find_one({"mail": mail})


    # CITATIONS

    def get_sorted_citation(self):
        output = []
        query = self._user.aggregate([{"$unwind": "$favorite"},{"$group": {"_id": "$favorite", "sum": {"$sum": 1}}},{"$limit" : 3 }])
        for doc in query:
            output.append(doc)
        return sorted(output, key=lambda k: k['sum'],reverse=True)

    def best_author(self):
        output = []
        query = self._citation.aggregate([{ "$group": {"_id": "$author", "count": { "$sum": 1}}},{"$sort": {"count": -1}},{"$limit": 1}] )
        for doc in query:
            output.append(doc)
        return output

    def best_user(self):
        output = []
        query = self._user.aggregate([{"$project":{" id": "$mail", "count": {"$size":{"$ifNull":["$mes_ajouts",[]]} } }},{"$sort" : {"count" : -1}},{"$limit" : 1 }])
        for doc in query:
            output.append(doc)
        return output

    def get_all_citations(self):
        print(self._citation.find({}))
        return list(self._citation.find({}))

    def add_citation(self, citation, author, oeuvre, date, langue, user):
        return self._citation.insert_one(
            {"text": citation, "author": author, "oeuvre": oeuvre, "date": date, "langue": langue, "added_by": user})

    def get_citation(self, id_citation):
        return self._citation.find_one({"_id": ObjectId(id_citation)})

    def get_citation_by_text(self, text):
        return self._citation.find_one({"text": text})

    def delete_citation(self, id_citation):
        return self._citation.delete_one({"_id": id_citation})
