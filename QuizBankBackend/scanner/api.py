import requests
import json
from QuizBankBackend import config


imgurUrl = 'https://api.imgur.com/3/image'
authHeader = 'Authorization'
clientId = config['ImgurClientId']

def uploadImage(image: str):
    payload = {'image': image}
    files = []
    headers = {authHeader: f'Client-ID {clientId}'}

    response = requests.post(imgurUrl, headers=headers, data=payload, files=files)

    return json.loads(response.text)

def deleteImage(deletehash: str):
    payload = {}
    files = []
    headers = {authHeader: f'Client-ID {clientId}'}

    response = requests.delete(f'{imgurUrl}/{deletehash}', headers=headers, data=payload, files=files)

    return response.text
