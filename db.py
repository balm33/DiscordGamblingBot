from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# """
# WILL LIKELY NEED TO CHANGE CLIENT FOR HEROKU USE
# """
# client = MongoClient("mongodb+srv://laptop:laptop-pass@footballpicker-cluster.yqjdz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# col = client.football_picks
# db = col.data

client = MongoClient(os.getenv("MONGODB_API_TOKEN"))
bjDB = client.blackjack.data

# insert object into database
def ins(userId, userCards, dealerCards, handActive, deck):
    dict = {
        "userId": userId,
        "userCards": userCards,
        "dealerCards": dealerCards,
        "isHandActive": handActive,
        "deck": deck
    }
    
    # checks if object already exists
    dup = bjDB.count_documents(dict)
    
    # if it does not exist create new object
    if dup <= 0:
        result = bjDB.insert_one(dict)
        print(f'Added to database with id {result.inserted_id}')
    # if it does exist replace data with updated data
    else:
        try:
            dataId = bjDB.find_one(dict)['_id']
            bjDB.replace_one({'_id': dataId}, dict)
            print(f"Replaced duplicate at id {dataId}")
        except Exception as e:
            print("No duplicates present", e)

def find(week, name):
    dict0 = {
        "week": week,
        "name": name
    }
    fnd = bjDB.find_one(dict0, {'_id': False})
    return fnd

# def find_all(week):
#     arr = []

#     cursor = db.find({"week": week}, {'_id': False})
#     for document in cursor:
#         arr.append(document)
#     return arr

ins(0, 0, 0, 0, 0)
