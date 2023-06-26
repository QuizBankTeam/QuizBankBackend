import json
from QuizBankBackend import app, config
from pymongo import MongoClient


client = MongoClient(config['MongodbUri'])
db = client.QuizBank
