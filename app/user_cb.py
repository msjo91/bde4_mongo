from datetime import datetime


class MyUser:
    def __init__(self, email, password, first_name, last_name, username, birth=None, phone=None, address=None):
        self.email = email
        self.password = password
        self.full_name = first_name + ' ' + last_name
        self.username = username
        self.birth = birth
        self.phone = phone
        self.address = address

    @classmethod
    def signup(cls):
        email = input('Enter email: ')
        password1 = input('Enter password: ')
        password2 = input('Confirm password: ')
        if password1 != password2:
            print('Both password inputs should match!')
            return
        first_name = input('Enter first name: ')
        if first_name is None:
            print('First name is required!')
            return
        last_name = input('Enter last name: ')
        if last_name is None:
            print('Last name is required!')
            return
        username = input('Enter username: ')
        birth = input('Enter Birthday in DD-MM-YYYY format (Optional): ')
        if birth is not None:
            bday, bmonth, byear = map(int, input("Enter birthday in DD-MM-YYYY format (optional): ").split('-'))
            try:
                birth = datetime(byear, bmonth, bday)
            except ValueError as e:
                print('    ' + str(e))
                return
        phone = input('Enter phone number: ')
        address = input('Enter address (Optional): ')
        return cls(
            email=email,
            password=password1,
            username=username,
            first_name=first_name,
            last_name=last_name,
            birth=birth,
            phone=phone,
            address=address
        )
