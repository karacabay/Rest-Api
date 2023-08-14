
import requests


class HealthCheck():
    def __init__(self, url):
        self.url = 'http://loadbalancer-1498206481.eu-north-1.elb.amazonaws.com/health'

    def __call__(self):
        r = requests.get(self.url)
        if r == 200:
            return True
        return False

health_check = HealthCheck()
flag = True
while flag:
    control = health_check()
    if control:
        print(control)
    

