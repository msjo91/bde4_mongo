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
            try:
                for j in i['posts']:
                    newsfeed.append([i['username'],j])
            except KeyError:
                pass
        if newsfeed:
            newsfeed2=sorted(newsfeed, key=lambda x: datetime.strptime(x[1]["date"],'%Y/%m/%d %H:%M:%S'),reverse=True)
            try:
                for i in range(0,k):
                    print("%s : "%newsfeed2[i][0], newsfeed2[i][1])
            except IndexError:
                print(" 더 볼 수있는 담벼락이 없습니다")

            enter=input("\n담벼락을 더 볼려면 1을 좋아요는 2, 싫어요는 3, 좋아요 취소는 4,싫어요 취소는 5, 메뉴로 나갈려면 아무키나 누르시오: " )

            if enter=="1":
                k+=2

            elif enter == "2":
                k = int(input("몇번째 뉴스피에 좋아요를 누르시겠습니까?"))
                try:
                    if db.users.find_one({"username":"%s"%newsfeed2[k-1][0], "posts":{"$elemMatch":{"date":newsfeed2[k-1][1]["date"],
                                                                                                "like_list":{"$in":[user]}}}}):
                        print("\n이미 좋아요를 눌렀습니다")
                    else:
                        db.users.update({"username":"%s"%newsfeed2[k-1][0],"posts.date":newsfeed2[k-1][1]["date"]}
                                    ,{'$inc':{'posts.$.like':1}})
                        db.users.update({"username": "%s" % newsfeed2[k - 1][0], "posts.date": newsfeed2[k - 1][1]["date"]}
                                    , {'$addToSet': {'posts.$.like_list':user}})
                except IndexError:
                    print("포스팅이 없습니다")

            elif enter == "3":
                k = int(input("몇번째 뉴스피에 싫어요를 누르시겠습니까?"))
                try:
                    if db.users.find_one({"username": "%s" % newsfeed2[k - 1][0],
                                      "posts": {"$elemMatch": {"date": newsfeed2[k - 1][1]["date"],
                                                               "hate_list": {"$in": [user]}}}}):
                        print("\n이미 싫어요를 눌렀습니다")
                    else:
                        db.users.update({"username":"%s"%newsfeed2[k-1][0],"posts.date":newsfeed2[k-1][1]["date"]}
                                        ,{'$inc':{'posts.$.hate':1}})
                        db.users.update({"username": "%s" % newsfeed2[k - 1][0], "posts.date": newsfeed2[k - 1][1]["date"]}
                                        , {'$addToSet': {'posts.$.hate_list': user}})
                except IndexError:
                    print("포스팅이 없습니다")



            elif enter == "4":
                k = int(input("몇번째 뉴스피에 좋아요를 취소하시겠습니까?"))
                try:
                    if db.users.find_one({"username": "%s" % newsfeed2[k - 1][0],
                                      "posts": {"$elemMatch": {"date": newsfeed2[k - 1][1]["date"],
                                                               "like_list": {"$in": [user]}}}}):
                        db.users.update({"username":"%s"%newsfeed2[k-1][0],"posts.date":newsfeed2[k-1][1]["date"]}
                                        ,{'$inc':{'posts.$.like':-1}})
                        db.users.update({"username": "%s" % newsfeed2[k - 1][0], "posts.date": newsfeed2[k - 1][1]["date"]}
                                        , {'$pull': {'posts.$.like_list': user}})
                    else:
                        print('좋아요를 누르지 않았습니다')
                except IndexError:
                    print("포스팅이 없습니다")


            elif enter == "5":
                k = int(input("몇번째 뉴스피드에 싫어요를 취소하시겠습니까?"))
                try:
                    if db.users.find_one({"username": "%s" % newsfeed2[k - 1][0],
                                      "posts": {"$elemMatch": {"date": newsfeed2[k - 1][1]["date"],
                                                               "hate_list": {"$in": [user]}}}}):
                        db.users.update({"username":"%s"%newsfeed2[k-1][0],"posts.date":newsfeed2[k-1][1]["date"]}
                                        ,{'$inc':{'posts.$.hate':-1}})
                        db.users.update({"username": "%s" % newsfeed2[k - 1][0], "posts.date": newsfeed2[k - 1][1]["date"]}
                                        , {'$pull': {'posts.$.hate_list': user}})
                    else:
                        print('싫어요를 누르지 않았습니다')
                except IndexError:
                    print("포스팅이 없습니다")
            else:
                break
        else:
            print("팔로워들의 포스팅이 없습니다")

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
