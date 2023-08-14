from flask import Flask
from flask_bcrypt import Bcrypt

from .mongodb_wrapper import MongoDBWrapper
import json


with open('config.json', 'r') as fp:
    cfg = json.load(fp)

mongodb = MongoDBWrapper(cfg['MongoDBConfig'])

app = Flask(__name__)
app.config['SECRET_KEY'] = cfg['AppSecretKey']

bcrypt = Bcrypt(app)

from . import routes