from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://4attye:upEIrWRmbcF1WVtn@clusters.s150f.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.test

MODES = {
    "show one": lambda: show_one(db),
    "show all": lambda: show_all(db),
    "update age": lambda: update_age(db),
    "update features": lambda: update_features(db),
    "delete cat": lambda: delete_cat(db),
    "delete all": lambda: delete_all(db),
    }

def main():
    while True:
        command = input("Введіть команду: ")
        match command:
            case "exit" | "close":
                break
            case _ if command in MODES:
                MODES[command]()
            case _:
                print("Invalid command")

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


def delete_cat(database):
    cat_name = input("Введіть ім'я кота: ")
    database.cats.delete_one({"name": cat_name})
    result = database.cats.find_one({"name": cat_name})
    print(result)


def delete_all(database):
    result = database.cats.delete_many({})
    print(result.deleted_count)


if __name__ == "__main__":
    main()
