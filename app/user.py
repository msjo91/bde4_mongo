from pymongo import MongoClient
from main import *

def signup(db):
    id=input("ID : ")
    password=input("password : ")
    confirm_password=input("confirm password : ")
    if password==confirm_password:
        if  users.find({"id":"%s"%id}):
            print("this id already exists.")
        else:
            users.insert({"ID":"%s"%id,"password":"%s"%password})
    else:
        print("confrim password is incorrect")

    '''
    1. Get his/her information.
    2. Check if his/her password equals confirm password.
    3. Check if the userid already exists.
    4. Make the user document.
    5. Insert the document into users collection.
    '''

#이름, 아이디, 비밀번호


def signin(db):
    id = input("ID : ")
    password = input("password : ")
    if users.find({"id":"%s"%id}):
        if users.find({"id":"%s"%id,"password":"%s"%id}):
            print("welcome")
            userpage(db,users)
        else:
            print("password incorrect")
    else:
        print("not exists id")


    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''


def mystatus(db, user):
    '''
    print user profile, # followers, and # followings
    '''

def userpage(db, user):
    '''
    user page
    '''


#이름, 비밀번호, 닉네임, 연락처, 주소 , 국적 , 성별, 한마디#