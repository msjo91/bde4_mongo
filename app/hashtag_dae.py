from main import *
from pymongo import *


def hashtag_search(db,user):
    #포스트적을떄 뛰어쓰기로 스플릿 그이후 #으로시작하는 단어는 해쉬리스트에 넣어줌
    #posts.hash로 텍스트인덱스생성, 그이후 hash를 가지고있는 document찾고 그document의 posts.hash안에 내가검색할려는 word있는지 확인
    #있으면 해쉬있는 포스트만검색,없으면 미검색

    while True:
        db.users.drop_indexes()
        db.users.create_index([('posts.hash', pymongo.TEXT)])
        word=input("Enter search in hashtag word : ")
        print()
        result=db.users.find({"$text":{'$search':'%s'%word}})
        search=[]
        for i in result:
            for j in i['posts']:
                if word in j['hash']:
                    search.append([i['username'],j])
        if search:
            try:
                search_list = sorted(search, key=lambda x: datetime.strptime(x[1]["date"], '%Y/%m/%d %H:%M:%S'),
                                    reverse=True)
                k=3
                while True:
                    try:
                        for i in range(k):
                            print(search_list[i][0],":",search_list[i][1])
                    except IndexError:
                        print("\n더볼 포스팅이 없습니다")
                    if input("포스팅 더 볼려면 1, 아니면 아무거나 누르세요 : ")=="1":
                        k+=2
                    else:
                        break
                break
            except KeyError:
                print("posts not exists")
                break
        else:
            print("\n해당 해쉬태그를 포함하는 포스팅이 없습니다\n")
            act=input("더 검색하실려면 1, 나갈거면 0을 누르세요 : ")
            if act=="0":
                break