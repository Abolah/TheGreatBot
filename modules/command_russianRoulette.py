import hikari
import tanjun
import random
import datetime
import time
from datetime import timezone
import pymongo
import sentry_sdk
import os


try:
    component = tanjun.Component()

    sentry_sdk.init(os.getenv("SENTRY"))
    mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
    mongoClient = pymongo.MongoClient(mongoURL)
    mongoExclusionCollection = mongoClient["TheGreatBot"]["tgbGlobalParameters"]

    if os.getenv("ENV") == "DEV":
        mongoRouletteLeaderboard = mongoClient["TheGreatBot"]["beta_tgbRouletteLDB"]
    else:
        mongoRouletteLeaderboard = mongoClient["TheGreatBot"]["tgbRouletteLDB"]


    @component.with_slash_command
    @tanjun.as_slash_command("roulette", "Joue un round de roulette russe. Si tu perds, tu es TO pendant 30 secondes.")
    async def commandRoulette(ctx: tanjun.abc.SlashContext, bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot), always_defer=True, default_to_ephemeral=False) -> None:
        start = time.perf_counter()
        allowedChannels = mongoExclusionCollection.find_one({})["rouletteAllowedChannels"]
        if ctx.channel_id in allowedChannels:
            member = ctx.member
            nickname = ctx.member.nickname
            roulette = ["Clic", "Clic", "Clic", "Clic", "Clic", "Pan"]
            rouletteResult = random.choice(roulette)
            if rouletteResult == "Clic":
                embed = (
                    hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0x14452f))
                        .set_thumbnail("https://media.giphy.com/media/AQRapWCgC7dThyVEYb/giphy.gif")
                        .add_field(name="*roulements de Tambours...*",
                            value="Bravo, tu as survécu cette fois. Retente ta chance plus tard.",
                            inline=False)
                )
                await ctx.respond(embed)
            elif rouletteResult == "Pan":
                if str(ctx.member) not in mongoExclusionCollection.find_one({})["rouletteImmuneUsers"]:
                    currentDatetime = datetime.datetime.now(timezone.utc)
                    newDatetime = currentDatetime + datetime.timedelta(seconds=3)
                    await bot.rest.edit_member(guild=ctx.guild_id, user=member, communication_disabled_until=newDatetime)
                    if str(ctx.member) == "kono_loki_da":
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Ben alors Loki, on est naze ? Ben ouais, t'as perdu. Cheh!",
                                inline=False)
                        )
                        await ctx.respond(embed=embed)
                    elif str(ctx.member) == "abolah":
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Imagine, tu codes le bot et tu perds à la roulette russe. Mdr imagine juste.",
                                inline=False)
                        )
                        await ctx.respond(embed=embed)
                    else:
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Machin truc a perdu au round de roulette russe !",
                                inline=False)
                        )
                        await ctx.create_initial_response(embed=embed, ephemeral=False)
                        #await ctx.respond(embed=embed)
                        end = time.perf_counter()
                        print("Time to run : ", end - start)
                else:
                    if str(ctx.member) == "thegreatreview":
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Les Saints Cheveux dévient la balle qui viens se loger dans la plante. Pense à l'arroser de temps en temps par pitié.",
                                inline=False)
                        )
                    elif str(ctx.member) == "milous98":
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Dès que le coup retentit, Milous attrape sa guitare et joue un solo de 10 minutes. La balle est déviée par le riff endiablé.",
                                inline=False)
                        )
                    elif str(ctx.member) == "pastequemayo":
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Bagon mange la balle. Pourquoi pas après tout ?",
                                inline=False)
                        )
                    elif str(ctx.member) == "epo.eitos":
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value="Epo ne peut pas mourir tout de suite. Il est papa et doit continuer une daronnade digne de ce nom.",
                                inline=False)
                        )
                    else:
                        embed = (
                            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0xc21807))
                            .set_thumbnail("https://media.giphy.com/media/60rGqeykp8O597gBNO/giphy.gif")
                            .add_field(name="*roulements de Tambours...*",
                                value=f"{member.mention} a perdu au round de roulette russe mais il est immunisé au TO. Ca compte quand même pour une lose.",
                                inline=False)
                        )
                    await ctx.respond(embed=embed)
        else:
            try:
                await ctx.respond("Tu ne peux pas jouer à la roulette russe ici. Va dans <#1196464488031989932>")
                #await ctx.create_initial_response("Tu ne peux pas jouer à la roulette russe ici. Va dans <#1227005935692681226>", ephemeral=True)
            except Exception as e:
                if os.getenv("ENV") == "DEV":
                    print("Error while trying to get message content with error : ", e)
                    print(ctx.message)
                else:
                    sentry_sdk.capture_exception(e)


    load_slash = component.make_loader()

except Exception as e:
    if os.getenv("ENV") == "DEV":
        print("Error loading module command_russianRoulette.py : ",  e)
    else:
        sentry_sdk.capture_exception(e)
