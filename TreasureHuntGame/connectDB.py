import pymongo

# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["game"]