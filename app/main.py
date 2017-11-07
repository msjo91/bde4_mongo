from pymongo import MongoClient

from member import signin, signup, signout, delete_account, profile, update_profile


def index_sign():
    print("\n===============================================================")
    print("    1. Sign In")
    print("    2. Sign Up")
    print("    0. Close")
    act = input("\nChoose an action: ")
    if act == "1":
        signin()
        index_main()
    elif act == "2":
        signup()
        index_main()
    elif act == "0":
        print("\nGood bye :D")
        client.close()
    else:
        "Error: Wrong command!"
        index_sign()


def index_main():
    print("\n===============================================================")
    print("    1. Profile")
    print("    9. Sign out")
    print("    0. Close")
    act = input("\nChoose an action: ")
    if act == "1":
        index_profile()
    elif act == "9":
        signout()
        index_sign()
    elif act == "0":
        print("\nGood bye :D")
        client.close()
    else:
        print("Error: Wrong command!")
        index_main()


def index_profile():
    print("\n===============================================================")
    print("    1. My Status")
    print("    2. Update Status")
    print("    9. Delete Account")
    print("    0. Main Page")
    act = input("\nChoose an action: ")
    if act == "1":
        profile()
        index_profile()
    elif act == "2":
        index_user_update()
        index_profile()
    elif act == "9":
        delete_account()
    elif act == "0":
        index_main()
    else:
        print("Error: Wrong command!")
        index_profile()


def index_user_update():
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
        update_profile(act)
    elif act == "0":
        index_main()
    else:
        print("Error: Wrong command!")
        index_user_update()


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
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
    index_sign()
