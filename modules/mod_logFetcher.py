import hikari
import tanjun
import base64
import os
import requests
import pymongo
from time import gmtime, strftime, sleep
from datetime import datetime
import sentry_sdk

try:
    sentry_sdk.init(os.getenv("SENTRY"))
    ip = requests.get('https://ifconfig.me/').content.decode('utf8')

    mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
    mongoClient = pymongo.MongoClient(mongoURL)

    if ip != os.environ.get("PROD_SERVER_IP"):
        mongoMemberLogsCollection = mongoClient["TheGreatBot"]["beta_tgbMessages"]
        mode = "DEV"
    else:
        mongoMemberLogsCollection = mongoClient["TheGreatBot"]["tgbMessages"]
        mode = "PROD"

    component = tanjun.Component()

    @component.with_slash_command
    @tanjun.with_member_slash_option("member", "member to fetch logs from", default=None)
    @tanjun.with_channel_slash_option("channel", "channel to fetch logs from", default=None)
    @tanjun.with_int_slash_option("limit", "limit of messages to fetch", default=10)
    @tanjun.with_str_slash_option("message_id", "ID of the messages to fetch", default=None)
    @tanjun.with_bool_slash_option("deleted", "fetch deleted messages", default=False)
    @tanjun.with_bool_slash_option("updated", "fetch updated messages", default=False)
    @tanjun.as_slash_command("getlogs", "Récupère les logs d'un utilisateur")
    async def mod_command_getLogs(ctx: tanjun.abc.SlashContext, member, channel, limit, message_id, deleted, updated) -> None:
        await ctx.respond("Commande en cours de développement")
        #verify if the user is an admin or has a role
        print(channel)
        print(limit)
        print(message_id)
        print(deleted)
        print(updated)
        # Fetch all documents in the Mongo databases
        if member is None and channel is None and message_id is None and deleted is False and updated is False:
            mongoLogs = mongoChannelsCollection.find().sort("Time", -1).limit(limit)
            for item in mongoLogs:
                print(item)
        elif member is None and channel is None and message_id is None and deleted is True and updated is False:
            mongoLogs = mongoChannelsCollection.find({"Deleted": True}).sort("Time", -1).limit(limit)
            for item in mongoLogs:
                print(item)
        elif member is None and channel is None and message_id is None and deleted is False and updated is True:
            mongoLogs = mongoChannelsCollection.find({"Updated": True}).sort("Time", -1).limit(limit)
            for item in mongoLogs:
                print(item)
        elif member is None and channel is None and message_id is None and deleted is True and updated is True:
            mongoLogs = mongoChannelsCollection.find({"Deleted": True, "Updated": True}).sort("Time", -1).limit(limit)
            for item in mongoLogs:
                print(item)
        query = {"Author": member.username, "MessageID": int(message_id), "Channel": str(channel.name), "Deleted": deleted, "Updated": updated}
        print(query)
        mongoLogs = mongoChannelsCollection.find(query).sort("Time", -1).limit(limit)
        for item in mongoLogs:
            print(item)

        embed = (
            hikari.Embed(title="Chat Logs", colour=hikari.Colour(0x005087), description="blablabla description")
                .set_footer(text="Hehehe",
                            icon="https://imagedelivery.net/9028nwfeen78DgldCtmuWg/ee25ecb7-d8ae-407b-f412-3547b4e67e00/public")
                .add_field(name="Abonnez vous", value="Poce blo", inline=False)
        )

        # await ctx.respond(embed)


    load_slash = component.make_loader()

except Exception as e:
    if prod:
        sentry_sdk.capture_exception(e)
    else:
        logger.error("Error while trying to load this module with error : ", e)
