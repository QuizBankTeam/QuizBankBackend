from QuizBankBackend import config
from pymongo import MongoClient


client = MongoClient(config['MongodbUri'])
db = client.QuizBank
