from pymongo import MongoClient

from member import signin, signup, signout


def logo():
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
    print("    9. Log out")
    print("    0. Close")
    act = input("\nChoose an action: ")
    if act == "1":
        pass
    elif act == "9":
        signout()
        index_sign()
    elif act == "0":
        print("\nGood bye :D")
        client.close()
    else:
        print("Error: Wrong command!")
        index_main()


if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    logo()
    index_sign()
