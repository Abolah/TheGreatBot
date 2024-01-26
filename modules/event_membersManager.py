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
from loguru import logger
import sentry_sdk

try:
    component = tanjun.Component()

    sentry_sdk.init(os.getenv("SENTRY"))

    mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
    mongoClient = pymongo.MongoClient(mongoURL)

    if os.getenv("ENV") == "DEV":
        mongoMembersCollection = mongoClient["TheGreatBot"]["beta_tgbMembers"]
    else:
        mongoMembersCollection = mongoClient["TheGreatBot"]["tgbMembers"]


    @component.with_listener()
    async def getMemberUpdateEvent(event: hikari.MemberUpdateEvent) -> None:
        try:
            oldMember = event.old_member
            query = {"memberID": event.member.id}
            MemberDocument = mongoMembersCollection.find_one(query)
            if MemberDocument is None:
                if event.member.nickname is None:
                    event.member.nickname = event.member.username
                oldNicknames = []
                query = {"memberID": event.member.id, "memberUsername": event.member.username,
                         "memberNickname": event.member.nickname, "memberOldNicknames": oldNicknames,
                         "JoinedAt": event.member.joined_at}
                mongoMembersCollection.insert_one(query)
            else:
                oldNicknames = MemberDocument["memberOldNicknames"]
                if not oldNicknames:
                    if event.member.nickname != event.old_member.nickname:
                        oldNicknames.append(oldMember.nickname)
                        query = {"memberID": event.member.id}
                        mongoMembersCollection.update_one(query, {"$set": {"memberNickname": event.member.nickname, "memberOldNicknames": oldNicknames}})
                    elif event.member.nickname is None:
                        if event.member.username != event.old_member.nickname:
                            oldNicknames.append(event.member.username)
                            query = {"memberID": event.member.id}
                            mongoMembersCollection.update_one(query, {
                                "$set": {"memberNickname": event.member.username, "memberOldNicknames": oldNicknames}})
                elif oldNicknames:
                    if event.member.nickname != event.old_member.nickname:
                        oldNicknames.append(oldMember.nickname)
                        query = {"memberID": event.member.id}
                        mongoMembersCollection.update_one(query, {
                            "$set": {"memberNickname": event.member.nickname, "memberOldNicknames": oldNicknames}})
                    elif event.member.nickname is None:
                        if event.member.username != event.old_member.nickname and event.old_member.nickname is not None:

                            oldNicknames.append(event.member.username)
                            query = {"memberID": event.member.id}
                            mongoMembersCollection.update_one(query, {
                                "$set": {"memberNickname": event.member.username, "memberOldNicknames": oldNicknames}})
        except Exception as e:
            if os.getenv("ENV") == "DEV":
                print("Error while trying to get message content with error : ", e)
                print(event.message)
            else:
                sentry_sdk.capture_exception(e)


    @component.with_listener()
    async def guildMemberJoinEvent(event: hikari.MemberCreateEvent) -> None:
        try:
            member = event.member
            if member.nickname is None:
                member.nickname = member.username
            query = {"memberID": member.id, "memberUsername": member.username,
                     "memberNickname": member.nickname, "memberOldNicknames": [],
                     "JoinedAt": member.joined_at}
            mongoMembersCollection.insert_one(query)
        except Exception as e:
            if os.getenv("ENV") == "DEV":
                print("Error while trying to get message content with error : ", e)
                print(event.message)
            else:
                sentry_sdk.capture_exception(e)


    @component.with_listener()
    async def guildMemberLeaveEvent(event: hikari.MemberDeleteEvent) -> None:
        try:
            member = event.old_member
            query = {"memberID": member.id}
            MemberDocument = mongoMembersCollection.find_one(query)
            if MemberDocument is None:
                query = {"memberID": member.id, "memberUsername": member.username,
                         "memberNickname": member.nickname, "memberOldNicknames": [],
                         "JoinedAt": member.joined_at, "LeftAt": datetime.now()}
                mongoMembersCollection.insert_one(query)
            else:
                query = {"memberID": member.id}
                mongoMembersCollection.update_one(query, {"$set": {"LeftAt": datetime.now()}})
        except Exception as e:
            if os.getenv("ENV") == "DEV":
                print("Error while trying to get message content with error : ", e)
                print(event.message)
            else:
                sentry_sdk.capture_exception(e)

    component = component.make_loader()
except Exception as e:
    if os.getenv("ENV") == "DEV":
        print("Error while trying to load event_memberManagers.py module with error : ", e)
    else:
        sentry_sdk.capture_exception(e)
