from pymongo import MongoClient
from user import *

def mainpage(db):
    '''
    call signup() or signin()
    '''
    N=int(input("기능을 입력하세요 :"))
    print("1. sing up")
    print("2. sing in")
    if N==1:
        signup(db)
    elif N==2:
        signin(db)

    #1은 계쩡생성
    #2는 로그인 뭐이런식

if __name__ == "__main__":
    '''
    call mainpage()
    '''
    client = MongoClient("localhost", 27017)
    db = client.project
    users = db.users
    mainpage(db)