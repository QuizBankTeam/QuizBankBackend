import json
from QuizBankBackend import app
from pymongo import MongoClient


db_file = open('QuizBankBackend/MONGODB_SETTING.json')
data = json.load(db_file)

client = MongoClient(data['uri'])
db = client.QuizBank
