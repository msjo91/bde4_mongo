from pymongo.errors import ConnectionFailure
import sys
from main import *
import pymongo
from datetime import datetime


def newsfeed(db,user):
    k=2
    while True:
        newsfeed = []
        newsfeed2 = []
        result=db.users.find({"follower list":{'$in':[user]}},{"username":1,"posts":1,"_id":0}).sort('posts.1')
        for i in result:
            for j in i['posts']:
                newsfeed.append([i['username'],j])
        print(newsfeed)
        newsfeed2=sorted(newsfeed, key=lambda x: datetime.strptime(x[1][1],'%Y/%m/%d %H:%M:%S'),reverse=True)
        print(newsfeed2)
        try:
            for i in range(0,k):
                print("%s : "%newsfeed2[i][0], newsfeed2[i][1])
        except IndexError:
            print(" 더 볼 수있는 담벼락이 없습니다")
        if input("\n 더 볼려면 1을 누르고 아니면 아무키나 누르세요 : ")=='1':
            k+=2
        else:
            break



def followpage(db,user):
    while True:
        print("\n===============================================================")
        print("    1. follow")
        print("    2. undfollow")
        print("    0. Close")
        act = input("\nChoose an action: ")
        if act=="1":
            followid=input("이름을 입력하세요: ")
            follow(db,user,followid)
        if act=="2":
            followid=input("이름을 입력하세요: ")
            unfollow(db,user,followid)
        if act=="0":
            break


def follow(db, user, followid):
    try:
        if user==followid:
            print("자기자신은 안된다")
        elif db.users.find_one({'username':followid}):
            if db.users.find_one({'username':user,"following list":{'$in':[followid]}}):
                print("있어..")
            else:
                db.users.update({"username":user},{'$push':{"following list":{'$each':[followid]}}})
                db.users.update({"username": followid}, {'$push': {"follower list":{'$each':[user]}}})
                db.users.update({"username":user},{'$inc':{"following":1}})
                db.users.update({"username": followid}, {'$inc': {"follower": 1}})
        else:
            print("그런사람 없어..")

        '''
        1. 팔로우하고자 하는 유저가 존재하는지 확인, 없으면 경고 출력

        2. 팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 있으면 경고 출력

        3. 팔로잉 목록에 없으면,
            나의 팔로잉 목록에 팔로우할 유저id 추가 + 상대방의 팔로워 목록에 내 id 추가
        '''
    except Exception as e:
        sys.stderr.write("could not operate following %s\n" %e)


def unfollow(db, user, followid):
    try:
        if user==followid:
            print("자기자신은 안된다")
        elif db.users.find_one({'username':followid}):
            if db.users.find_one({'username': user, "following list": {'$in': [followid]}}):
                db.users.update({"username":user},{"$pull":{"following list":followid}})
                db.users.update({"username": followid}, {"$pull": {"follower list":user}})
                db.users.update({"username": user}, {'$inc': {"following": -1}})
                db.users.update({"username": followid}, {'$inc': {"follower": -1}})
            else:
                print("팔로잉 안되있어")
        else:
            print("그런사람 없어..")
        '''
        1. 언팔로우하고자하는 유저가 존재하는지 확인, 없으면 경고 출력

        2. 언팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 없으면 경고 출력

        3. 팔로잉 목록에 있으면,
            나의 팔로잉 목록에서 언팔로우할 유저id 제거 + 상대방의 팔로워 목록에서 내 id 제거
        '''
    except Exception as e:
        sys.stderr.write("could not operate following %s\n" %e)
