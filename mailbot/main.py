
import requests


class HealthCheck():
    def __init__(self, url):
        self.url = 'http://16.171.129.13:80'

    def __call__(self):
        r = requests.get(self.url)
        if r == 200:
            return True
        return False

health_check = HealthCheck()
flag = True
while flag:
    if health_check():

