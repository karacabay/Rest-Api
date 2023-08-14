
import requests
import json
import random


def list_card_info(user_no, auth_code, endpoint):
    headers = {
        'UserNo': str(user_no),
        'Authorization': auth_code
    }
    return requests.post(url+endpoint, headers=headers)


with open('../config.json', 'r') as fp:
    server_cfg = json.load(fp)['ServerConfig']
server_cfg['Host'] = '16.171.129.13'
url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"
url = 'http://13.48.149.251:80'
url = 'http://localhost:8080'
user_no = 2250058
auth_code = 'qUiiNr3uzc'
endpoint='/list-card-info'

r = list_card_info(user_no, auth_code, endpoint)
print(r.content)
# data = json.loads(r.content)
# print(data)

