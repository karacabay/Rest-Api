
import requests
import json
import random


def list_card_info(user_no, auth_code, endpoint):
    headers = {
        'UserNo': str(user_no),
        'Authorization': auth_code
    }
    return requests.post(url+endpoint, headers=headers)


url = 'http://loadbalancer-1498206481.eu-north-1.elb.amazonaws.com'
user_no = 2250058
auth_code = 'qUiiNr3uzc'
endpoint='/list-card-info'

r = list_card_info(user_no, auth_code, endpoint)
print(r)
try :
    data = json.loads(r.content)
    print(data)
except:
    pass
