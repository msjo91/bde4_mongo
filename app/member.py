from datetime import datetime

from pymongo import MongoClient

users = MongoClient('localhost', 27017).bde4_sns.member

online = []


def signin():
    print("\n::::SIGN IN::::\n")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if users.find_one({"username": username, "password": password}):
        online.append(username)
        print("Welcome, %s" % username)
    else:
        print("    User does not exist or wrong password input!")
        signin()


def signup():
    print("\n::::SIGN UP::::\n")
    username = input("Enter username: ")
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
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            full_name = first_name + ' ' + last_name
            bday, bmonth, byear = map(int, input("Enter birthday in DD-MM-YYYY format: ").split('-'))
            try:
                birth = datetime(byear, bmonth, bday)
            except ValueError as e:
                print('    ' + str(e))
                signup()
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")
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


def delete():
    print("\n::::DELETE ACCOUNT::::\n")
    username = online[0]
    password = input("Enter password: ")
    if users.find_one({"username": username, "password": password}):
        verification = input("Are you sure? ")
        if verification in ['y', 'Y', 'yes', 'Yes']:
            users.remove({'username': username})
            print("We had a good run, %s! We'll miss you :(" % online.pop())
