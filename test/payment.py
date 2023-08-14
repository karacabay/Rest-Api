
import requests
import json
import random


def payment(user_no, auth_code, card_number, total_amount, endpoint, is_selected=False):
    headers = {
        'UserNo': str(user_no),
        'Authorization': auth_code
    }
    data = {
        'Card': str(card_number),
        'IsSelected': is_selected,
        'TotalAmount': total_amount
    }
    json_data = json.dumps(data)
    return requests.post(url+endpoint, headers=headers, json=json_data)


with open('../config.json', 'r') as fp:
    server_cfg = json.load(fp)['ServerConfig']

url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"

user_no = 82967981
auth_code = 'XeH7AklA8x'
card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
endpoint='/payment'
total_amount = 813
is_selected = True

r = payment(user_no, auth_code, card_number, total_amount, endpoint, is_selected)
print(r.content)

