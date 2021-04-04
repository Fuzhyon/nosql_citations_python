from pymongo import MongoClient


def get_db():
    client = MongoClient('localhost:27017')
    db_mongo = client.citations_db
    return db_mongo


# USER

def get_all_user(db_mongo):
    collection = db_mongo.user
    return list(collection.find({}))


def add_user(db_mongo, name, mail, password):
    db_mongo.user.insert_one({"name": name, "mail": mail, "pwd": password})


def get_user(db_mongo):
    return db_mongo.user.find_one()


# CITATIONS

def get_all_citations(db_mongo):
    collection = db_mongo.citation
    return list(collection.find({}))
