from datetime import datetime

from pymongo import MongoClient

users = MongoClient('localhost', 27017).bde4_sns.member

online = []


def signin():
    while 1:
        print("\n::::SIGN IN::::\n")
        username = input("Enter username or type exit to exit: ")
        if username == 'exit':
            break
        password = input("Enter password: ")
        if users.find_one({"username": username, "password": password}):
            online.append(username)
            print("Welcome, %s" % username)
        else:
            print("    User does not exist or wrong password input!")
            signin()


def signup():
    while 1:
        print("\n::::SIGN UP::::\n")
        username = input("Enter username or type exit to exit: ")
        if username == 'exit':
            break
        password = input("Enter password: ")
        if not password:
            print("    You must insert a password!")
            signup()
        password_confirm = input("Confirm password: ")
        if password == password_confirm:
            if users.find_one({"username": username}):
                print("    User already exists!")
                signup()
            else:
                first_name = input("Enter first name (optional): ")
                last_name = input("Enter last name (optional): ")
                full_name = first_name + ' ' + last_name
                bday, bmonth, byear = map(int, input("Enter birthday in DD-MM-YYYY format (optional): ").split('-'))
                try:
                    birth = datetime(byear, bmonth, bday)
                except ValueError as e:
                    print('    ' + str(e))
                    signup()
                email = input("Enter email (optional): ")
                phone = input("Enter phone number (optional): ")
                address = input("Enter address (optional): ")
                users.insert({
                    "username": username,
                    "password": password,
                    "name": full_name,
                    "first name": first_name,
                    "last name": last_name,
                    "birth": birth,
                    "email": email,
                    "phone": phone,
                    "address": address
                })
                print("User creation success!")
                signin()
        else:
            print("Passwords don't match!")
            signup()


def signout():
    print("See you again, %s" % online.pop())


def profile():
    while 1:
        print("\n::::MY STATUS::::\n")
        username = online[0]
        if users.find_one({"username": username}):
            cursor = users.find_one({"username": username})
            print("""
            Username: {username}
            Name: {name}
            Birthday: {birth}
            Email: {email}
            Phone: {phone}
            Address: {address}
            """.format(
                username=username,
                name=cursor['name'],
                birth=str(cursor['birth']).split()[0],
                email=cursor['email'],
                phone=cursor['phone'],
                address=cursor['address']
            ))
        else:
            print("    Wrong password input!")
            profile()


def update_profile(act):
    d = {"1": "first name", "2": "last name", "3": "birth", "4": "email", "5": "phone", "6": "address", "9": "password"}
    print("\n::::UPDATE PROFILE::::\n")
    username = online[0]
    password = input("Enter password: ")
    if users.find_one({"username": username, "password": password}):
        if act == "3":
            bday, bmonth, byear = map(int, input("Enter new birthday in DD-MM-YYYY format: ").split('-'))
            try:
                birth = datetime(byear, bmonth, bday)
                users.update({"username": username}, {"$set": {"birth": birth}})
                print("Update Success!")
            except ValueError as e:
                print('    ' + str(e))
                update_profile(act)
        else:
            new = input("Enter new %s: " % d[act])
            users.update({"username": username}, {"$set": {d[act]: new}})
            if act == "1" or act == "2":
                first_name = users.find_one({"username": username})["first name"]
                last_name = users.find_one({"username": username})["last name"]
                full_name = first_name + ' ' + last_name
                users.update({"username": username}, {"$set": {"name": full_name}})
                print("Update Success!")
            elif act == "9":
                new_confirm = input("Confirm password: ")
                if new == new_confirm:
                    print("Update Success!")
                else:
                    print("Passwords don't match!")
                    update_profile(act)
            else:
                print("Update Success!")
    else:
        print("    Wrong password input!")
        update_profile(act)


def delete_account():
    print("\n::::DELETE ACCOUNT::::\n")
    username = online[0]
    password = input("Enter password: ")
    if users.find_one({"username": username, "password": password}):
        verification = input("Are you sure? ")
        if verification in ['y', 'Y', 'yes', 'Yes']:
            users.remove({'username': username})
            print("We had a good run, %s! We'll miss you :(" % online.pop())
    else:
        print("    Wrong password input!")
        delete_account()
