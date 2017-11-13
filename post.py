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
        print("    1. My posts list")
        print("    2. Insert Post")
        print("    3. Delete Post")
        print("    0. retun page")
        act = input("\nChoose an action: ")
        if act == "1":
            mypostslist(db,user)
        elif act == "2":
            insertPost(db,user)
        elif act == "3":
            deletePost(db,user)
        elif act == "0":
            break
        else:
            "Error: Wrong command!"

def mypostslist(db,user):
    while True:
        t = db.users.find_one({"username": user})
        for i in t['posts']:
            print(i)
        act = input("\n좋아요 명단을 볼려면 1,싫어요 명단을 보려면 2를 나갈려면 아무키나 누르세요 : ")
        if act=="1":
            for i in t['posts']:
                print(i)
            k=int(input("\n좋아요 명단을 보고싶은 포스팅을 선택해주세요 : "))
            try:
                print('\n',t['posts'][k - 1]['like_list'], '\n')
            except KeyError:
                print("\n없다\n")
        elif act=="2":
            for i in t['posts']:
                print(i)
            k = int(input("\n싫어요 명단을 보고싶은 포스팅을 선택해주세요 : "))
            try:
                print('\n',t['posts'][k-1]['hate_list'],'\n')
            except KeyError:
                print("\n없다\n")

        else:
            break


def insertPost(db,user):
    while True:
        t=db.users.find_one({"username": user})
        for i in t['posts']:
            print(i)
        now=datetime.datetime.now()
        index = "%d/%d/%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        k=input("하고싶은 말 입력하세요 : ")
        db.users.update({"username": user}, {"$push":{"posts":{"post":k,"date":index}}})
        break


def deletePost(db,user):
    while True:
        t = db.users.find_one({"username": user})
        for i in t['posts']:
            print(i)
        date=input("\n삭제하고 싶은 포스트의 시간을 입력하세요 (ex:2017/01/10 11:23:11) : ")
        db.users.update({"username": user},{"$pull":{"posts":{"date":date}}})
        break

    """
    Delete user's text.
    With the post schema, you can remove posts by some conditions that you specify.
    """

    """
    Sometimes, users make a mistake to insert or delete their text.
    We recommend that you write the double-checking code to avoid the mistakes.
    """
