import datetime
import os
from pathlib import Path
import hikari
import tanjun
import requests
import logs
import sentry_sdk
from colorama import Fore
from datadog import initialize, statsd
from loguru import logger

global MODE

if os.name != "nt":
    import uvloop
    uvloop.install()

ip = requests.get('https://ifconfig.me/').content.decode('utf8')
sentry_sdk.init(os.getenv("SENTRY"))


BASEDIR = os.path.abspath(os.path.dirname(__file__))

if ip != os.environ.get("PROD_SERVER_IP"):
    MODE = "DEV"
else:
    MODE = "PROD"


def CreateBot() -> hikari.GatewayBot:
    if MODE == "DEV":
        print(Fore.YELLOW + "Running in DEV mode" + Fore.RESET)
        bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.getenv("DISCORD"), logs="DEBUG")
        client = tanjun.Client.from_gateway_bot(bot, declare_global_commands=427939132984000544)
    else:
        bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.getenv("DISCORD"), logs="WARNING")
        client = tanjun.Client.from_gateway_bot(bot)
    module_path = os.path.join(BASEDIR, 'modules')
    try:
        print(Fore.GREEN + "Loading modules" + Fore.YELLOW + " from " + module_path + Fore.RESET)
        client.load_modules(*Path(module_path).glob("*.py"))
        logger.info("Modules loaded")
    except Exception as exceptionDetails:
        logger.error("Error while loading modules with details : ", exceptionDetails)
        sentry_sdk.capture_exception(exceptionDetails)

    return bot


if os.name != "nt":
    import uvloop
    uvloop.install()

CreateBot().run()
