
import requests
import time
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(n):
    # Mail Hesap Bilgileri
    sender_email = "casestudy343@gmail.com"
    password = "fbmkyyrukbfxcmkv"

    # Kime Gönderilecek Bilgisi
    receiver_email = "deveneskaracabay@gmail.com"

    # E-posta konfigürasyonu
    subject = "connection error".upper()
    message = f"Unable to establish a connection to the server {n}."

    # E-posta oluşturma
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # E-posta gönderme
    try:
        server = SMTP('smtp.gmail.com', 587)  # E-posta sağlayıcınıza göre ayarlayın
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)


class HealthCheck():
    def __init__(self, url):
        self.counter = 0
        self.url = url

    def __call__(self):
        try:
            r = requests.get(self.url)
        except:
            self.counter += 1
            return False
        
        if r.status_code == 200:
            self.reset_counter()
            return True
        
        self.counter += 1
        return False
    
    def reset_counter(self):
        self.counter = 0
    

url_1 = 'http://13.48.149.251/health'
url_2 = 'http://16.171.129.13/health'


health_check_1 = HealthCheck(url_1)
health_check_2 = HealthCheck(url_2)

flag = True
while flag:
    control_1 = health_check_1()
    if not control_1:
        if health_check_1.counter == 3:
            send_mail('http://13.48.149.251')

    control_2 = health_check_2()
    if not control_2:
        if health_check_2.counter == 3:
            send_mail('http://16.171.129.13')

    time.sleep(5)
    




