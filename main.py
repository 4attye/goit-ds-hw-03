from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://4attye:upEIrWRmbcF1WVtn@clusters.s150f.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.animals

MODES = {
    "show one": lambda: show_one(db),
    "show all": lambda: show_all(db),
    "update age": lambda: update_age(db),
    "update features": lambda: update_features(db),
    "delete cat": lambda: delete_one(db),
    "delete all": lambda: delete_all(db),
    "help": lambda: help(),
    }

def main():
    print("Щоб переглянути всі команди введіть команду 'help'")
    while True:
        command = input("Введіть команду: ")
        match command:
            case "exit" | "close":
                break
            case _ if command in MODES:
                MODES[command]()
            case _:
                print("Invalid command")

def help():
    print("""
        'show one' - показує данні кота за його ім'ям
        'show all' - показує всі данні в колекції
        'update age' - оновлює вік кота за його ім'ям
        'update features' - додає особливість кота за його ім'ям
        'delete cat' - видаляє данні кота за цого ім'ям
        'delete all' - видаляє всі данні з колекції
        'exit' або 'close' - команди які завершують роботу скрипта
    """)

def show_all(dbase):
    result = dbase.cats.find({})
    for el in result:
        print(el)


def show_one(dbase):
    cat_name = input("Введіть ім'я кота: ")
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def update_age(dbase):
    cat_name = input("Введіть ім'я кота: ")
    cat_age = input("Введіть вік кота: ")
    dbase.cats.update_one({"name": cat_name}, {"$set": {"age": cat_age}})
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def update_features(dbase):
    cat_name = input("Введіть ім'я кота: ")
    cat_features = input("Введіть особливість кота: ")
    dbase.cats.update_one({"name": cat_name}, {"$push": {"features": cat_features}})
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def delete_one(dbase):
    cat_name = input("Введіть ім'я кота: ")
    dbase.cats.delete_one({"name": cat_name})
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def delete_all(dbase):
    result = dbase.cats.delete_many({})
    print(result.deleted_count)


if __name__ == "__main__":
    main()
