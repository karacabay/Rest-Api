
import json
from typing import Any
import requests
import random
import string
import random
import random
from datetime import datetime, timedelta


def add_new_document(admin, password, document, endpoint):
    headers = {
        'Admin': admin,
        'Password': password,
    }
    json_data = json.dumps(document)
    return requests.post(url+endpoint, headers=headers, json=json_data)



class GenerateRandomDocument():

    def __init__(self):
        turkish_names = [
            "Ahmet", "Ayşe", "Mustafa", "Fatma", "Ali", "Zeynep",
            "Mehmet", "Emine", "Hüseyin", "Hatice", "Hasan", "Sultan",
            "İbrahim", "Sema", "Yusuf", "Esra", "Osman", "Derya",
            "Ayhan", "Elif", "Murat", "Gizem", "Ertuğrul", "Merve",
            "Tolgahan", "Ceren", "Eren", "Aslı", "Cemal", "Selma",
            "Volkan", "Nur", "İsmail", "Zehra", "Kemal", "Leyla",
            "Hakan", "Aysel", "Hilal", "Özgür", "Nihan", "Kadir",
            "Sevgi", "Fikret", "Sibel", "Okan", "Beyza", "Cihan",
            "Rabia", "Levent", "Gül", "Tolga", "Melike", "Oğuz"
        ]

        turkish_surnames = [
            "Yılmaz", "Kaya", "Demir", "Çelik", "Aydın", "Arslan",
            "Kara", "Kurt", "Koç", "Aksoy", "Taş", "Eren", "Şahin",
            "Toprak", "Güneş", "Keskin", "Doğan", "Bulut", "Çetin",
            "Yıldız", "Aslan", "Cengiz", "Bıçak", "Baş", "Güler",
            "Tuncer", "Gür", "Duman", "Gül", "Kaplan", "Kılıç",
            "Duru", "Oğuz", "Uçar", "Kurtuluş", "Kartal", "Deniz",
            "Atasoy", "Kocaman", "Koçak", "Kır", "Yavuz", "Yıldırım",
            "Okan", "Kapıcı", "Erdem", "Usta", "Küçük", "Kanat", "Soy"
        ]
        self.turkish_names_surnames = list(zip(turkish_names, turkish_surnames))
        self.start_datetime = datetime(2019, 1, 1, 0, 0, 0)  
        self.end_datetime = datetime(2023, 7, 31, 23, 59, 59)
        self.b_end_date = datetime(2004, 12, 30)
        self.b_start_date = datetime(1960, 1, 1)
        self.counter = 0

    def __call__(self):

        self.docs = list()
        for _ in range(len(self.turkish_names_surnames)):
            tmp = self.generate_one()
            self.docs.append(tmp)

        return self.docs

    def generate_one(self):
        
        cards_length = random.randint(1, 5)
        allCards = list()

        for _ in range(cards_length):
            tmp_card_number = str()
            for _ in range(16):
                char = random.randint(0, 9)
                tmp_card_number += str(char)
            allCards.append(tmp_card_number)
        name = self.turkish_names_surnames[self.counter][0]
        surname = self.turkish_names_surnames[self.counter][1]

        user_no = random.randint(10000, 100000000)
        is_userno_unique = False if len(self.docs) != 0 else True
        while not is_userno_unique:
            old_user_no_list = [row['userNo'] for row in self.docs]
            if user_no not in old_user_no_list:
                is_userno_unique = True

        tmp_date1 = self.generate_random_datetime()
        tmp_date2 = self.generate_random_datetime()
        if tmp_date1 > tmp_date2:
            created_on = tmp_date2
            updated_on = tmp_date1
        else:
            created_on = tmp_date1
            updated_on = tmp_date2

        self.counter += 1

        return {
            "userNo": user_no,
            "authCode": self.generate_random_string(10),
            "name": name,
            "surname": surname,
            "birthDate": self.generate_birth_date(),
            "phoneNumber": random.randint(5300000000, 5499999999),
            "email": f'{name}{surname}@email.com',
            "selectedCard":random.choice(allCards), 
            "allCards": allCards,
            "balance": random.randint(10, 100000),
            "createdOn": created_on,
            "updatedOn": updated_on,
            "onProcess": False
        }
    
    def generate_random_string(self, length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    
    def generate_random_datetime(self):
        time_between_datetimes = self.end_datetime - self.start_datetime
        seconds_between_datetimes = time_between_datetimes.total_seconds()
        random_number_of_seconds = random.randrange(seconds_between_datetimes)
        random_datetime = self.start_datetime + timedelta(seconds=random_number_of_seconds)
        return random_datetime.timestamp()
    
    def generate_birth_date(self):
        time_between_dates = self.b_end_date - self.b_start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = self.b_start_date + timedelta(days=random_number_of_days)
        return random_date.timestamp()

with open('../config.json', 'r') as fp:
    server_cfg = json.load(fp)['ServerConfig']

url = f"http://{server_cfg['Host']}:{server_cfg['Port']}"

admin = 'admin'
password = '!o43g=!cmd'

document_generator = GenerateRandomDocument()
documents = document_generator()

for document in documents:
    r = add_new_document(admin, password, document, endpoint='/add-new-document')
    print(r.content)


