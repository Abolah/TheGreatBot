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

sentry_sdk.init(os.getenv("SENTRY"))


BASEDIR = os.path.abspath(os.path.dirname(__file__))
MODE = os.getenv("ENV")


def CreateBot() -> hikari.GatewayBot:
    if MODE == "DEV":
        print(Fore.YELLOW + "Running in DEV mode" + Fore.RESET)
        bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.getenv("DISCORD"), logs="DEBUG")
        client = tanjun.Client.from_gateway_bot(bot, declare_global_commands=427939132984000544)
    else:
        import schedulers
        bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.getenv("DISCORD"), logs="WARNING")
        client = tanjun.Client.from_gateway_bot(bot, declare_global_commands=True)
    module_path = os.path.join(BASEDIR, 'modules')
    try:
        client.load_modules(*Path(module_path).glob("*.py"))
    except Exception as exceptionDetails:
        logger.error("Error while loading modules with details : ", exceptionDetails)
        sentry_sdk.capture_exception(exceptionDetails)
    logger.info("Modules loaded")

    return bot


if os.name != "nt":
    import uvloop
    uvloop.install()

CreateBot().run()
