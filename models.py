import pymongo
from passlib.hash import pbkdf2_sha256
# from wtforms import SubmitField,ValidationError
myclient = pymongo.MongoClient("mongodb+srv://sumit:sumitsarkar@cluster0.c5xwu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

chatDB = myclient.get_database("chatdb")
users=chatDB.get_collection('users')
rooms=chatDB.get_collection('room_id')
def get_username():
    return users
def get_roomid():
    l=[]
    for i in rooms.find():
        l.append(i['room_id'])
    return l
        