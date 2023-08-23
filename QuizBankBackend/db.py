from QuizBankBackend import config
from pymongo import MongoClient


client = MongoClient(config['MongodbUri'], connect = False)
db = client.QuizBank
