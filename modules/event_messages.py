import hikari
import tanjun
import toolbox
import requests
import base64
import os
import pymongo
from time import gmtime, strftime
from datetime import datetime
from time import sleep


component = tanjun.Component()

ip = requests.get('https://ifconfig.me/').content.decode('utf8')
mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
mongoClient = pymongo.MongoClient(mongoURL)

if ip != os.environ.get("PROD_SERVER_IP"):
    mongoMemberLogsCollection = mongoClient["TheGreatBot"]["beta_tgbMessages"]

else:
    mongoMemberLogsCollection = mongoClient["TheGreatBot"]["tgbMessages"]
    prod


@component.with_listener()
async def getTextMessage(event: hikari.GuildMessageCreateEvent, bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
    try:
        if not event.message.author.is_bot:
            try:
                messageTime = datetime.strptime(datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                messageID = event.message.id
                messageContent = event.message.content
                messageChannel = str(await bot.rest.fetch_channel(bot.cache.get_guild_channel(event.message.channel_id)))
                messageAuthor = event.message.author.username
                messageObject = await bot.rest.fetch_message(event.message.channel_id, event.message.id)
                if messageObject.attachments:
                    messageMediaList = []
                    for attachment in messageObject.attachments:
                        attachmentURL = attachment.url
                        messageMedia = base64.b64encode(requests.get(attachmentURL).content).decode("utf-8")
                        messageMediaList.append(messageMedia)
                    mongoUChannelsDict = {"Author": messageAuthor, "Message": messageContent, "MessageID": messageID, "Channel": messageChannel, "Time": messageTime, "Media": messageMediaList, "Deleted": False, "Updated": False}
                else:
                    mongoUChannelsDict = {"Author": messageAuthor, "Message": messageContent, "MessageID": messageID, "Channel": messageChannel, "Time": messageTime, "Deleted": False, "Updated": False}
                try:
                    mongoMemberLogsCollection.insert_one(mongoUChannelsDict)
                except Exception as e:
                    if prod:
                        sentry_sdk.capture_exception(e)
                    else:
                        logger.error("Error while trying to insert new Message in MongoDB with error : ", e)
                        print("Error while trying to insert new Message in MongoDB with error : ", e)
            except Exception as e:
                if prod:
                    sentry_sdk.capture_exception(e)
                else:
                    logger.error("Error while trying to get message content with error : ", e)
                    print("Error while trying to get message content with error : ", e)
    except Exception as e:
        if prod:
            sentry_sdk.capture_exception(e)
        else:
            logger.error("Error while trying to get message content with error : ", e)
            print("Error while trying to get message content with error : ", e)
            print(event.message)


@component.with_listener()
async def getUpdatedMessage(event: hikari.GuildMessageUpdateEvent, bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
    try:
        if event.message.author:
            if not event.message.author.is_bot:
                try:
                    messageTime = datetime.strptime(datetime.now().isoformat(), "%Y-%m-%dT%H:%M:%S.%f")
                    messageID = event.message.id
                    messageContent = event.message.content
                    messageChannel = str(await bot.rest.fetch_channel(bot.cache.get_guild_channel(event.message.channel_id)))
                    messageAuthor = event.message.author.username
                    messageObject = await bot.rest.fetch_message(event.message.channel_id, event.message.id)
                    if messageObject.attachments:
                        messageMediaList = []
                        for attachment in messageObject.attachments:
                            attachmentURL = attachment.url
                            messageMedia = base64.b64encode(requests.get(attachmentURL).content).decode("utf-8")
                            messageMediaList.append(messageMedia)
                        mongoUChannelsDict = {"Author": messageAuthor, "Message": messageContent, "MessageID": messageID,
                                              "Channel": messageChannel, "Time": messageTime, "Media": messageMediaList, "Deleted": False, "Updated": True}
                    else:
                        mongoUChannelsDict = {"Author": messageAuthor, "Message": messageContent, "MessageID": messageID,
                                              "Channel": messageChannel, "Time": messageTime, "Deleted": False, "Updated": True}
                    try:
                        mongoMemberLogsCollection.insert_one(mongoUChannelsDict)
                        # print("New Message inserted in MongoDB with data : ", mongoUChannelsDict)
                    except Exception as e:
                        logger.error("Error while trying to insert new Message in MongoDB with error : ", e)
                        print("Error while trying to insert new Message in MongoDB with error : ", e)
                except Exception as e:
                    logger.error("Error while trying to get message content with error : ", e, "\n and Message Informations: ", event.message.author, event.message.content, event.message.id, event.message.channel_id, event.message.attachments)
                    print("Error while trying to get message content with error : ", e, "\n and Message Informations: ", event.message.author, event.message.content, event.message.id, event.message.channel_id, event.message.attachments)
    except Exception as e:
        if prod:
            sentry_sdk.capture_exception(e)
        else:
            print("Error while trying to get message content with error : ", e)
            print(event.message)


@component.with_listener()
async def getDeletedMessage(event: hikari.GuildMessageDeleteEvent) -> None:
    messageID = event.message_id
    query = {"MessageID": messageID}
    mongoMemberLogsCollection.update_many(query, {"$set": {"Deleted": True}})

try:
    component = component.make_loader()
except Exception as e:
    print("Error while trying to load the getLogs command with error : ", e)
    pass
