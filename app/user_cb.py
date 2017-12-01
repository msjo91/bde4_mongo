from datetime import datetime

from connection_cb import Conn

db = Conn


class User:
    def __init__(self, email, password, username, first_name, last_name, birth=None, phone=None, address=None):
        self.email = email
        self.password = password
        self.username = username
        self.full_name = first_name + ' ' + last_name
        self.birth = birth
        self.phone = phone
        self.address = address

    @classmethod
    def signup(cls):
        email = input('Enter email: ')
        if email is None:
            print('\tError: Email is required!')
            return
        elif '@' not in email:
            print('\tError: This is not an email!')
            return
        elif db.users.find_one({'email': email}):
            print("\tError: Email already registered!")
            return
        password1 = input('Enter password: ')
        if password1 is None:
            print('\tError: Password is required!')
            return
        password2 = input('Confirm password: ')
        if password1 != password2:
            print('\tError: Both passwords should match!')
            return
        username = input('Enter username: ')
        if username is None:
            print('\tError: Username is required!')
            return
        first_name = input('Enter first name: ')
        if first_name is None:
            print('\tError: First name is required!')
            return
        last_name = input('Enter last name: ')
        if last_name is None:
            print('\tError: Last name is required!')
            return
        birth = input('Enter Birthday in yyyy-mm-dd format (Optional): ')
        if birth is not None:
            year, month, day = map(int, birth.split('-'))
            try:
                birth = datetime(year, month, day)
            except ValueError as e:
                print('\tError: ' + str(e))
                return
        phone = input('Enter phone number (Optional): ')
        address = input('Enter address (Optional): ')
        new_user = cls(
            email=email,
            password=password1,
            username=username,
            first_name=first_name,
            last_name=last_name,
            birth=birth,
            phone=phone,
            address=address
        )
        return db.users.insert({'user': {new_user}})

    def signin(self):
        email = input('Enter email: ')
        password = input('Enter password: ')
        if db.users.find_one({'user': {}})
