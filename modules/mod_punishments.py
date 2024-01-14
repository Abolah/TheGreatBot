import hikari
import tanjun
import base64
import os
import requests
import pymongo
from time import gmtime, strftime, sleep
from datetime import datetime

import hikari
import tanjun

ip = requests.get('https://ifconfig.me/').content.decode('utf8')
mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
mongoClient = pymongo.MongoClient(mongoURL)

if ip != os.environ.get("PROD_SERVER_IP"):
    mongoPunishmentsCollection = mongoClient["TheGreatBot"]["beta_tgbPunishments"]
else:
    mongoPunishmentsCollection = mongoClient["TheGreatBot"]["tgbPunishments"]


component = tanjun.Component()
try:

    load_slash = component.make_loader()
except Exception as e:
    print("Error while trying to load the getLogs command with error : ", e)
    #sentry_sdk.capture_exception(e)
    pass
