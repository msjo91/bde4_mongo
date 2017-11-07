from pymongo import MongoClient
from main import *
from user import *
import datetime

def postInterface(db,user):

    """
    Implementing the interface to post your text.
    There are three or more items to choose functions such as inserting and deleting a text.
    """
    while True:
        t = db.users.find_one({"username": user})
        try:
            print("My Posts List : \n\n",t["posts"])
        except KeyError :
            print("\nPosts not exists")
        print("\n===============================================================")
        print("    1. Insert Post")
        print("    2. Delete Post")
        print("    0. retun page")
        act = input("\nChoose an action: ")
        if act == "1":
            insertPost(db,user)
        elif act == "2":
            deletePost(db,user)
        elif act == "0":
            break
        else:
            "Error: Wrong command!"


def insertPost(db,user):
    while True:
        t=db.users.find_one({"username": user})
        now=datetime.datetime.now()
        index = "%d/%d/%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        k=input("하고싶은 말 입력하세요 : ")
        db.users.update({"username": user}, {"$push":{"posts":[k,index]}})
        break


def deletePost(db,user):
    while True:
        t = db.users.find_one({"username": user})
        print(t['posts'])
        date=input("\n삭제하고 싶은 포스트의 시간을 입력하세요 (ex:2017/01/10 11:23) : ")
        db.users.update({"username": user},{"$pull":{"posts":{"$in":[date]}}})
        break

    """
    Delete user's text.
    With the post schema, you can remove posts by some conditions that you specify.
    """

    """
    Sometimes, users make a mistake to insert or delete their text.
    We recommend that you write the double-checking code to avoid the mistakes.
    """
