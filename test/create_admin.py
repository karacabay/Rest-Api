
import requests
import json


def create_admin(admin, password, endpoint):
    headers = {
        'Admin': admin,
        'Password': password
    }
    return requests.post(url+endpoint, headers=headers)


with open('../config.json', 'r') as fp:
    server_cfg = json.load(fp)['ServerConfig']

url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"

# admin = 'admin'
# password = '!o43g=!cmd'
# create_admin(admin, password, endpoint='/create-admin-user')
