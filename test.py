import requests

url = 'https://quizbank.soselab.tw/login'

response = requests.post(url, data={'username': 'test', 'password': 'test'})
print(response.status_code)