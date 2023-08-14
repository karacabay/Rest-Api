
import requests
import json
import random


def add_new_card(user_no, auth_code, card_number, endpoint, is_selected=True):
    headers = {
        'UserNo': str(user_no),
        'Authorization': auth_code
    }
    data = {
        'Card': str(card_number),
        'IsSelected': is_selected
    }
    json_data = json.dumps(data)
    u = url+endpoint

    return requests.post(u, headers=headers, json=json_data)


with open('../config.json', 'r') as fp:
    server_cfg = json.load(fp)['ServerConfig']

url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"
url = 'http://loadbalancer-1498206481.eu-north-1.elb.amazonaws.com'

user_no = 2250058
auth_code = 'qUiiNr3uzc'
card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
endpoint='/add-new-card'
is_selected = True

r = add_new_card(user_no, auth_code, card_number, endpoint, is_selected)
print(r.content)

