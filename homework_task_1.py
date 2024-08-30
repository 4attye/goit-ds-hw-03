from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://4attye:upEIrWRmbcF1WVtn@clusters.s150f.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.animals


def show_all(database):
    result = database.cats.find({})
    for el in result:
        print(el)


def show_one(database):
    cat_name = input("Введіть ім'я кота: ")
    result = database.cats.find_one({"name": cat_name})
    print(result)


def update_age(database):
    cat_name = input("Введіть ім'я кота: ")
    cat_age = input("Введіть вік кота: ")
    database.cats.update_one({"name": cat_name}, {"$set": {"age": cat_age}})
    result = database.cats.find_one({"name": cat_name})
    print(result)


def update_features(database):
    cat_name = input("Введіть ім'я кота: ")
    cat_features = input("Введіть особливість кота: ")
    database.cats.update_one({"name": cat_name}, {"$push": {"features": cat_features}})
    result = database.cats.find_one({"name": cat_name})
    print(result)


def delete_one(database):
    cat_name = input("Введіть ім'я кота: ")
    database.cats.delete_one({"name": cat_name})
    result = database.cats.find_one({"name": cat_name})
    print(result)


def delete_all(database):
    result = database.cats.delete_many({})
    print(result.deleted_count)


show_all(db)
show_one(db)
update_age(db)
update_features(db)
delete_one(db)
delete_all(db)
