from pymongo import *
from main import *
from datetime import *

def message(db,user):
    while True:
        print("\n===============================================================")
        print("    1. Message Confirmation")
        print("    2. Send Message")
        print("    0. retun page")
        act = input("\nChoose an action: ")
        if act=="1":
            message_confirm(db,user)
        elif act=="2":
            send_message(db,user)
        elif act=="0":
            break

def message_confirm(db,user):
    #메세지는 전유저에게 다보낼수 있음, 유저목록에있으면 그유저와 나눴던 메세지들확인가능
    #자기자신과는 메세지확인불가 기본3개까지볼수있고 더보기가능 +2개씩 추가
    while True:
        search = db.users.find({}, {'username': 1, '_id': 0})
        user_list = []
        for i in search:
            user_list.append(i['username'])
        for i in user_list:
            print("Username : ", i)

        friend = input("\n누구와의 메세지를 확인 하시겠습니까? : ")

        if friend==user:
            print("자기자신과의 메세지는 없습니다.")
            break
        else:
            if friend in user_list:
                    search=db.users.find_one({"username":user,"message.Reciever":friend})
                    result=[]
                    try:
                        for i in search['message']:
                            if i['Reciever']==friend:
                                result.append(i)
                    except TypeError:
                        print("%s와 주고받은 메세지가 없습니다"%friend)
                        break
                    message_list = sorted(result, key=lambda x: datetime.strptime(x["date"], '%Y/%m/%d %H:%M:%S'), reverse=True)
                    k=3
                    while True:
                        try:
                            for i in range(k):
                                print(message_list[i])
                        except IndexError:
                            print("메세지가 더이상 없습니다")
                        act=input("메세지를 더 볼려면 1, 아니면 아무키나 누르세요 : ")
                        if act=="1":
                            k+=2
                        else:
                            break
                    break
            else:
                print("\n유저 목록에 없는 사람입니다.\n")
                break



def send_message(db,user):
    #유저목록에 유저있는지 검색하고 유저목록에 존재하는유저면 메세지 보내기 가능
    while True:
        now = datetime.now()
        index = "%d/%d/%d %d:%d:%d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        search=db.users.find({},{'username':1,'_id':0})
        user_list=[]
        for i in search:
            user_list.append(i['username'])
            print("username :", i['username'])

        friend=input("메세지 보내려는 친구의 이름을 입력하세요 : ")

        if friend in user_list:
            contents=input("내용을 입력하세요 : ")
            if friend != user:
                db.users.update({"username": user}, {"$push": {"message": {"Sender":user, "Reciever": friend,"Contents": contents,"date": index}}})
                db.users.update({"username": friend}, {"$push": {"message": {"Sender": friend, "Reciever": user,"Contents": contents, "date": index}}})
                break
            else:
                print("\n나 자신에게 메세지 보낼 수 없습니다\n")
                break
        else:
            print("\n유저 목록에 없는 사람입니다.\n")
            break
