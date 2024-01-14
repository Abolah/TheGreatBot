import hikari
import tanjun
import base64
import os
import requests
import pymongo
from time import gmtime, strftime, sleep
from datetime import datetime

try:

    ip = requests.get('https://ifconfig.me/').content.decode('utf8')
    mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
    mongoClient = pymongo.MongoClient(mongoURL)

    if ip != os.environ.get("PROD_SERVER_IP"):
        mongoPunishmentsCollection = mongoClient["TheGreatBot"]["beta_tgbPunishments"]
    else:
        mongoPunishmentsCollection = mongoClient["TheGreatBot"]["tgbPunishments"]
        prod

    component = tanjun.Component()

    load_slash = component.make_loader()

except Exception as e:
    if prod:
        sentry_sdk.capture_exception(e)
    else:
        logger.error("Error while trying to load this module with error : ", e)

