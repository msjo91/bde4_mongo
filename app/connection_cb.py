from pymongo import MongoClient


class Conn:
    def __init__(self):
        self.db = MongoClient('localhost', 27017).sns
        self.users = self.db.users
        self.posts = self.db.posts

    def save(self):
        pass
