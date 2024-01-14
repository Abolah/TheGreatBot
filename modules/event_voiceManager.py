import hikari
import tanjun
import toolbox
from time import sleep
import os
import pymongo
import sentry_sdk

try:
    component = tanjun.Component()

    sentry_sdk.init(os.getenv("SENTRY"))
    mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
    mongoClient = pymongo.MongoClient(mongoURL)
    mongoChannelsCollection = mongoClient["TheGreatBot"]["tgbChannels"]
    MemberChannelsDict = {}
    Category = [1126999482144399381, 1122945192157261935]  # 2 catégories sont hardcodées pour le moment, Abodev & C&V, a changer plus tard (mongo ?)
    navette = [1125898837173731389, 1126999532060811367]
    Permissions = {}


    @component.with_listener()
    async def JoinVoiceChannel(event: hikari.VoiceStateUpdateEvent, bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
        member = await bot.rest.fetch_member(event.state.guild_id, event.state.user_id)
        if event.state.channel_id is not None:  #This means the user joined a voice channel
            if bot.cache.get_guild_channel(event.state.channel_id).parent_id in Category:
                if event.state.channel_id in navette:
                    categorychannel = await bot.rest.fetch_channel(bot.cache.get_guild_channel(event.state.channel_id).parent_id) #Fetch l'objet Channel de la catégorie
                    print("User {} joined a spaceship".format(member.username)) #User joined a spaceship
                    # Add logging later to MongoDB
                    memberPerms = toolbox.members.calculate_permissions(member=member, channel=categorychannel)
                    Permissions[member.username] = memberPerms
                    try:
                        await bot.rest.edit_permission_overwrite(channel=event.state.channel_id, target=member, deny=hikari.Permissions(1048576)) #Remove access to the spaceship
                        print("User {} has been denied access to the spaceship.".format(member.username))
                        newVoiceChannel = await bot.rest.create_guild_voice_channel(guild=event.state.guild_id, name=str(member.username), position=69420, category=bot.cache.get_guild_channel(event.state.channel_id).parent_id) #Create a new voice channel
                        print("New voice channel created with ID : {}".format(newVoiceChannel.id))
                        await bot.rest.edit_permission_overwrite(channel=newVoiceChannel.id, target=member, allow=hikari.Permissions(549792515600))  # Give more perms to the new voice channel
                        print("User {} has been granted access to the new voice channel.".format(member.username))
                        MemberChannelsDict[member.username] = {"CreatedVoiceChannel": newVoiceChannel.id, "OriginalVoiceChannel": event.state.channel_id} #This adds the member and its associated channels to the dict
                        mongoUChannelsDict = {"Channel": newVoiceChannel.id, "Members": []}
                        try:
                            mongoChannelsCollection.insert_one(mongoUChannelsDict)
                            print("New Channel inserted in MongoDB with data : ", mongoUChannelsDict)
                        except Exception as e:
                            print("Error while trying to insert new Channel in MongoDB with error : ", e)
                            #sentry_sdk.capture_exception(e)
                        await bot.rest.edit_member(guild=event.state.guild_id, user=member,voice_channel=newVoiceChannel.id)  # This moves the user to the new  voice channel
                        print("User {} moved to the new voice channel.".format(member.username))
                    except Exception as e:
                        print("Error while trying to create new Channel with error : ", e)

                else:
                    print("User {} joined a voice channel that is registered but not the navette with ID : {}".format(member.username, event.state.channel_id))
                    query = {"Channel": event.state.channel_id}
                    ChannelDocument = mongoChannelsCollection.find_one(query)
                    newArray = [member.username]
                    for registeredMember in ChannelDocument["Members"]:
                        newArray.append(registeredMember)
                    newDoc = {"$set": {"Members": newArray}} #This adds the member to the list of members in the channel
                    mongoChannelsCollection.update_one(query, newDoc)
                    #Add logging later to MongoDB
            else:
                print("User {} joined a voice channel that is NOT registered".format(member.username))
                #Add logging later to MongoDB
        else:
            # User left a voice channel
            await LeftVoiceChannel(bot, event, MemberChannelsDict)


    async def LeftVoiceChannel(bot, event, MemberChannelsDict) -> None:
        member = await bot.rest.fetch_member(event.state.guild_id, event.state.user_id)
        print("User {} left a voice channel.".format(member.username))
        #Add logging later to MongoDB
        # check if member is part of any document stored in mongo
        alLChannels = mongoChannelsCollection.find()
        for channelDoc in alLChannels:
            if member.username in channelDoc["Members"]:
                print("User {} is part of the channel {}.".format(member.username, channelDoc["Channel"]))
                channelDoc["Members"].remove(member.username)
                newDoc = {"$set": {"Members": channelDoc["Members"]}}
                mongoChannelsCollection.update_one({"Channel": channelDoc["Channel"]}, newDoc)
                print("User {} removed from the list of members of the channel {}.".format(member.username, channelDoc["Channel"]))
            else:
                print("User {} is not part of the channel {}.".format(member.username, channelDoc["Channel"]))
        # if yes, remove him from the list of members
        # if the list is empty, delete the channel
        # if no, give modification perms of the channel to the first member of the member array in the document
        try:
            if MemberChannelsDict[member.username] is not None:
                originalVoiceChannel = bot.cache.get_guild_channel(MemberChannelsDict[member.username]["OriginalVoiceChannel"])
                VoiceChannel = bot.cache.get_guild_channel(MemberChannelsDict[member.username]["CreatedVoiceChannel"])
                sleep(0.5)
                try:
                    await bot.rest.delete_channel(VoiceChannel.id)
                except Exception as e:
                    print("Error while trying to delete Channel with error : ", e)
                try:
                    await bot.rest.edit_permission_overwrite(channel=originalVoiceChannel, target=member, allow=hikari.Permissions(Permissions[member.username]))
                    print("User {} has been granted access to the spaceship.".format(member.username))
                except Exception as e:
                    print("Error while trying to grant access to the spaceship with error : ", e)
                MemberChannelsDict.pop(member.username)
                print("Voice channel deleted.")
            else:
                print("User didn't move in a voice channel.".format(member.username))
        except KeyError:
            return None

    component = component.make_loader()

except Exception as e:
    logger.error("Error while trying to load event_voiceManager.py module with error : ", e)
    sentry_sdk.capture_exception(e)

