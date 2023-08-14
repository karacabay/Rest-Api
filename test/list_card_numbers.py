
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

url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"

user_no = 82967981
auth_code = 'XeH7AklA8x'
endpoint='/list-card-info'

r = list_card_info(user_no, auth_code, endpoint)
data = json.loads(r.content)
print(data)

