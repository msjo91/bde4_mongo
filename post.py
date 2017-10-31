from pymongo import MongoClient
from main import *
from user import *

def postInterface(db):
    """
    Implementing the interface to post your text.
    There are three or more items to choose functions such as inserting and deleting a text.
    """
    while True:
        print("\n===============================================================")
        print("    1. Insert Post")
        print("    2. Delete Post")
        print("    0. retun page")
        act = input("\nChoose an action: ")
        if act == "1":
            insertPost(db)
            break
        elif act == "2":
            deletePost(db)
            break
        elif act == "0":
            break
        else:
            "Error: Wrong command!"


def insertPost(db):
    username = online[0]
    k=input("하고싶은 말 입력하세요 : ")
    db.users.update({"username": username}, {"$push": {"posts":{k}}})
	

def deletePost(db):
    """
    Delete user's text.
    With the post schema, you can remove posts by some conditions that you specify.
    """

    """
    Sometimes, users make a mistake to insert or delete their text.
    We recommend that you write the double-checking code to avoid the mistakes.
    "
