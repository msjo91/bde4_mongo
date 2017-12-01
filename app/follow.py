import sys

from pymongo import MongoClient

from member import online

users = MongoClient('localhost', 27017).bde4_sns.member


def follow(db, userid, followid):
    try:
        '''
        1. 팔로우하고자 하는 유저가 존재하는지 확인, 없으면 경고 출력

        2. 팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 있으면 경고 출력

        3. 팔로잉 목록에 없으면,
            나의 팔로잉 목록에 팔로우할 유저id 추가 + 상대방의 팔로워 목록에 내 id 추가
        '''
        if not users.find_one({"username": followid}):
            print("User does not exist.")
        else:
            if followid in users.find_one({"username": online[0]})['following']:
                print("User already following.")
            else:
                users.update({"username": online[0]}, {"$push": {"following": {"$each": followid}}})
                users.update({"username": followid}, {"$push": {"follower": {"$each": online[0]}}})
    except Exception as e:
        sys.stderr.write("Could not operate following %s\n" % e)


def unfollow(db, userid, followid):
    try:
        '''
        1. 언팔로우하고자하는 유저가 존재하는지 확인, 없으면 경고 출력

        2. 언팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 없으면 경고 출력

        3. 팔로잉 목록에 있으면,
            나의 팔로잉 목록에서 언팔로우할 유저id 제거 + 상대방의 팔로워 목록에서 내 id 제거
        '''
        if followid not in users.find_one({"username": online[0]})['following']:
            print("User is not in following list.")
        else:
            users.update({"username": online[0]}, {"$pull": {"following": {"$each": followid}}})
            users.update({"username": followid}, {"$pull": {"follower": {"$each": online[0]}}})
    except Exception as e:
        sys.stderr.write("Could not operate following %s\n" % e)
