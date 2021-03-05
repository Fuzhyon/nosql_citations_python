from pymongo import MongoClient

# Mongo
def get_db():
    client = MongoClient('localhost:27017')
    db = client.citations_db
    print(db.user.find_one())
    return db


def get_all_user(db):
    collection = db.user
    return list(collection.find({}))


def add_user(db):
    db.user.insert_one({"name": "Patrick", "mail": "patrick@mail.com", "pwd": "azerty"})
    db.user.insert_one({"name": "Gustave", "mail": "gustave@mail.com", "pwd": "azety"})
    db.user.insert_one({"name": "Thierry", "mail": "thierry@mail.com", "pwd": "aerty"})
    db.user.insert_one({"name": "John", "mail": "john@mail.com", "pwd": "azert"})
    db.user.insert_one({"name": "Ultimatron", "mail": "ultimatron@mail.com", "pwd": "zerty"})


def get_country(db):
    return db.user.find_one()