from pymongo import MongoClient

def get_db():
    client = MongoClient('localhost:27017')
    db_mongo = client.citations_db
    return db_mongo



def get_all_user(db_mongo):
    collection = db_mongo.user
    return list(collection.find({}))


def add_user(db_mongo):
    db_mongo.user.insert_one({"name": "Patrick", "mail": "patrick@mail.com", "pwd": "azerty"})
    db_mongo.user.insert_one({"name": "Gustave", "mail": "gustave@mail.com", "pwd": "azety"})
    db_mongo.user.insert_one({"name": "Thierry", "mail": "thierry@mail.com", "pwd": "aerty"})
    db_mongo.user.insert_one({"name": "John", "mail": "john@mail.com", "pwd": "azert"})
    db_mongo.user.insert_one({"name": "Ultimatron", "mail": "ultimatron@mail.com", "pwd": "zerty"})


def get_user(db_mongo):
    return db_mongo.user.find_one()


def get_all_citations(db_mongo):
    collection = db_mongo.citation
    return list(collection.find({}))