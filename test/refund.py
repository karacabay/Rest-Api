
import requests
import json
import random


def refund(user_no, auth_code, refund_amount, endpoint):
    headers = {
        'UserNo': str(user_no),
        'Authorization': auth_code
    }
    data = {
        'RefundAmount': refund_amount
    }
    json_data = json.dumps(data)
    return requests.post(url+endpoint, headers=headers, json=json_data)


with open('../config.json', 'r') as fp:
    server_cfg = json.load(fp)['ServerConfig']

url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"

user_no = 82967981
auth_code = 'XeH7AklA8x'
endpoint='/refund'
refund_amount = 999

r = refund(user_no, auth_code, refund_amount, endpoint)
print(r.content)

