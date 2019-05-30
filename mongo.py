from pymongo import MongoClient

class Mongo:
    user = ""
    password = ""
    uri = "localhost"
    port = 27017

    # def __init__():

    def init(self):
        return MongoClient(self.uri, self.port)