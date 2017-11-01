from pymongo import MongoClient
from user import *
from post import *



def index_sign(db):
    while True:
        print("\n===============================================================")
        print("    1. Sign In")
        print("    2. Sign Up")
        print("    0. Close")
        act = input("\nChoose an action: ")
        if act == "1":
            signin(db)
            break
        elif act == "2":
            signup(db)
        elif act == "0":
            print("\nGood bye :D")
            client.close()
            break
        else:
            "Error: Wrong command!"
    if online:
        index_main(db)
    else:
        index_sign(db)

def index_main(db):
    logout=False
    user=online[0]
    while True:
        print("\n===============================================================")
        print("    1. Profile")
        print("    2. Post Interface")
        print("    9. Log out")
        print("    0. Close")
        act = input("\nChoose an action: ")
        if act == "1":
            index_profile(db,user)
            break
        if act == "2":
            postInterface(db,user)
        elif act == "9":
            logout=True
            break
        elif act == "0":
            print("\nGood bye :D")
            online.pop()
            client.close()
            break
        else:
            print("Error: Wrong command!")
    if logout:
        signout(db)
        index_sign(db)
    elif online:
        index_main(db)
    else:
        index_sign(db)


def index_profile(db,user):
    delete=False
    while (1):
        print("\n===============================================================")
        print("    1. My Status")
        print("    2. Update Status")
        print("    9. Delete Account")
        print("    0. Main Page")
        act = int(input("\nChoose an action: "))
        if act == 1:
            profile(db,user)
        elif act == 2:
            index_user_update(db,user,act)
        elif act == 9:
            delete=True
            break
        elif act == 0:
            break
        else:
            print("Error: Wrong command!")
    if delete:
        delete_account(db,user)


def index_user_update(db,user,act):
    while True:
        print("\n===============================================================")
        print("    1. First name")
        print("    2. Last name")
        print("    3. Birthday")
        print("    4. Email")
        print("    5. Phone")
        print("    6. Address")
        print("    9. Password")
        print("    0. Main Page")
        act = input("\nChoose an action: ")
        if act in ["1", "2", "3", "4", "5", "6", "9"]:
            update_profile(db,user,act)
        elif act == "0":
            break
        else:
            print("Error: Wrong command!")


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db=client.sns
    users=db.users
    print("===============================================================")
    print("===============================================================")
    print("        __  ___                           _____ _   _______")
    print("       /  |/  /___  ____  ____ _____     / ___// | / / ___/")
    print("      / /|_/ / __ \/ __ \/ __ `/ __ \    \__ \/  |/ /\__ \ ")
    print("     / /  / / /_/ / / / / /_/ / /_/ /   ___/ / /|  /___/ /")
    print("    /_/  /_/\____/_/ /_/\__, /\____/   /____/_/ |_//____/")
    print("                       /____/")
    print("===============================================================")
    print("===============================================================")
    print("\n    Welcome to Mongo SNS!")
    print("    A mock terminal SNS designed for MongoDB application!")
    index_sign(db)