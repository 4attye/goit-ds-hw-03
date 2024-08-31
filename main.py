from colorama import Fore
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://4attye:upEIrWRmbcF1WVtn@clusters.s150f.mongodb.net/", server_api=ServerApi('1'))

db = client.animals

MODES = {
    "insert": lambda : insert(db),
    "show one": lambda: show_one(db),
    "show all": lambda: show_all(db),
    "update age": lambda: update_age(db),
    "update features": lambda: update_features(db),
    "delete cat": lambda: delete_one(db),
    "delete all": lambda: delete_all(db),
    "help": lambda: help(),
    }


def help():
    print(f"""{Fore.GREEN}
        'insert' - записує данні в БД
        'show one' - показує данні кота за його ім'ям
        'show all' - показує всі данні в колекції
        'update age' - оновлює вік кота за його ім'ям
        'update features' - додає особливість кота за його ім'ям
        'delete cat' - видаляє данні кота за цого ім'ям
        'delete all' - видаляє всі данні з колекції
        'exit' або 'close' - команди які завершують роботу скрипта {Fore.RESET}
    """)


def insert(dbase):
    cat_name = input(f"{Fore.BLUE}Введіть ім'я кота: {Fore.RESET}")
    cat_age = int(input(f"{Fore.BLUE}Введіть вік кота: {Fore.RESET}"))
    cat_features =  input(f"{Fore.BLUE}Введіть особливості кота через кому: {Fore.RESET}")
    dbase.cats.insert_one({
        "name": cat_name,
        "age": cat_age,
        "features": [f for f in cat_features.split(",")]
    })





def show_all(dbase):
    result = dbase.cats.find({})
    for el in result:
        print(el)


def show_one(dbase):
    cat_name = input(f"{Fore.BLUE}Введіть ім'я кота: {Fore.RESET}")
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def update_age(dbase):
    cat_name = input(f"{Fore.BLUE}Введіть ім'я кота: {Fore.RESET}")
    cat_age = input(f"{Fore.BLUE}Введіть вік кота: {Fore.RESET}")
    dbase.cats.update_one({"name": cat_name}, {"$set": {"age": cat_age}})
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def update_features(dbase):
    cat_name = input(f"{Fore.BLUE}Введіть ім'я кота: {Fore.RESET}")
    cat_features = input(f"{Fore.BLUE}Введіть особливість кота: {Fore.RESET}")
    dbase.cats.update_one({"name": cat_name}, {"$push": {"features": cat_features}})
    result = dbase.cats.find_one({"name": cat_name})
    print(result)


def delete_one(dbase):
    cat_name = input(f"{Fore.BLUE}Введіть ім'я кота: {Fore.RESET}")
    dbase.cats.delete_one({"name": cat_name})
    print(f"{Fore.BLUE}Видалено!{Fore.RESET}")


def delete_all(dbase):
    result = dbase.cats.delete_many({})
    print(result.deleted_count)


def main():
    print(f"{Fore.YELLOW}Щоб переглянути всі команди введіть команду{Fore.GREEN} 'help'{Fore.RESET}")
    while True:
        command = input(f"{Fore.BLUE}Введіть команду: {Fore.RESET}")
        match command:
            case "exit" | "close":
                break
            case _ if command in MODES:
                MODES[command]()
            case _:
                print(f"{Fore.RED}Invalid command{Fore.RESET}")


if __name__ == "__main__":
    main()
