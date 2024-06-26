import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
from tcp_latency import measure_latency
import sentry_sdk
from loguru import logger


sentry_sdk.init(os.getenv("SENTRY"))


def pingStatusPage():
    latency = measure_latency(host='discord.com')
    url = "https://uptime.abolah.dev/api/push/0Tjx3UlAdx?status=up&msg=OK&ping={}".format(str(latency[0]).split('.')[0])
    try:
        requests.get(url)
    except Exception as e:
        logger.error("Error while pinging StatusPage with URL : {} and error : {}".format(url, e))
        sentry_sdk.capture_exception(e)


scheduler = BackgroundScheduler()
if os.getenv("ENV") == "PROD":
    scheduler.add_job(pingStatusPage, "interval", seconds=19, timezone="Europe/Paris", max_instances=3)

scheduler.start()
