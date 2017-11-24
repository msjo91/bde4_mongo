from pymongo import MongoClient
from main import *
from user import *
from datetime import *


def postInterface(db,user):

    """
    Implementing the interface to post your text.
    There are three or more items to choose functions such as inserting and deleting a text.
    """
    while True:
        t = db.users.find_one({"username": user})
        try:
            posts_list = sorted(t['posts'], key=lambda x: datetime.strptime(x["date"], '%Y/%m/%d %H:%M:%S'), reverse=True)
            print("My Posts List : \n\n")
            for i in posts_list:
                print(i)
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
        try:
            posts_list = sorted(t['posts'], key=lambda x: datetime.strptime(x["date"], '%Y/%m/%d %H:%M:%S'),
                            reverse=True)
            for i in posts_list:
                print(i)
        except KeyError:
            print("posts not exists")
            break
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
        now=datetime.now()
        index = "%d/%d/%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        k=input("하고싶은 말 입력하세요 : ")
        hashing=[]
        for i in k.split(" "):
            if i[0]=="#":
                hashing.append(i[1:])
        db.users.update({"username": user}, {"$push":{"posts":{"post":k,"date":index,"hash":hashing}}})
        break


def deletePost(db,user):
    while True:
        t = db.users.find_one({"username": user})
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
