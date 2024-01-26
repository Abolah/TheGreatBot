import hikari
import tanjun
import base64
import os
import pymongo
from time import gmtime, strftime, sleep
from datetime import datetime, timezone, timedelta
import sentry_sdk

try:
    sentry_sdk.init(os.getenv("SENTRY"))
    mongoURL = "mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority".format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWD"), os.getenv("MONGO_CLUSTER"), os.getenv("MONGO_DB"))
    mongoClient = pymongo.MongoClient(mongoURL)

    if os.getenv("ENV") == "DEV":
        mongoPunishmentsCollection = mongoClient["TheGreatBot"]["beta_tgbPunishments"]
    else:
        mongoPunishmentsCollection = mongoClient["TheGreatBot"]["tgbPunishments"]

    component = tanjun.Component()

    @component.with_slash_command
    @tanjun.with_member_slash_option("member", "Membre à avertir")
    @tanjun.with_int_slash_option("days", "Nombre de jours pendant lesquels le membre sera TO. Par défaut, 0.", default=0)
    @tanjun.with_int_slash_option("hours", "Nombre d'heures pendant lesquelles le membre sera TO. Par défaut, 0.", default=0)
    @tanjun.with_int_slash_option("minutes", "Nombre de minutes pendant lesquelles le membre sera TO. Par défaut, 0.", default=0)
    @tanjun.with_int_slash_option("secondes", "Nombre de secondes pendant lesquelles le membre sera TO. Par défaut, 30.", default=30)
    @tanjun.with_str_slash_option("mod_reason", "Raison de l'avertissement donné à l'utilisateur. Par défaut, aucune raison.", default="Aucune raison donnée.")
    @tanjun.with_str_slash_option("user_reason", "Raison de l'avertissement. Par défaut, aucune raison.",
                                  default="Aucune raison donnée.")
    @tanjun.with_author_permission_check(1099511627776, error=None, error_message="Tu n'as pas les permissions pour utiliser cette commande.", follow_wrapped=False)
    @tanjun.as_slash_command("warn", "Averti un utilisateur et applique un TO d'une durée personnalisée. Par défaut, sera TO 30 secondes.")
    async def commandeWarn(ctx: tanjun.abc.SlashContext, member, days, hours, minutes, secondes, mod_reason, user_reason, bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
        now = datetime.now(timezone.utc)
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=secondes)
        end = now + delta
        try:
            warnedMember = mongoPunishmentsCollection.find_one({"member": str(member)})
            if warnedMember is None:
                query = {"member": member.username, "memberID": member.id, "warnNumber": 1, "warnReasons": [str(mod_reason)], "warnDates": [now]}
                mongoPunishmentsCollection.insert_one(query)
            else:
                warnNumber = warnedMember["warnNumber"]
                warnNumber += 1
                warnReasons = warnedMember["warnReasons"]
                warnReasons.append(str(mod_reason))
                warnDates = warnedMember["warnDates"]
                warnDates.append(now)
                query = {"member": member.username, "memberID": member.id, "warnNumber": warnNumber, "warnReasons": warnReasons, "warnDates": warnDates}
                mongoPunishmentsCollection.update_one({"member": member.username}, {"$set": query})
        except TypeError:
            query = {"member": member.username, "memberID": member.id, "warnNumber": 1, "warnReasons": [str(mod_reason)], "warnDates": [now]}
            mongoPunishmentsCollection.insert_one(query)
        ChannelDMWithMember = await bot.rest.create_dm_channel(member)
        await ChannelDMWithMember.send("Bonsoir {},\nVous avez recu un avertissement par {} pour la raison suivante :\n {}".format(member, ctx.member.username, user_reason))

        await bot.rest.edit_member(guild=ctx.guild_id, user=member, communication_disabled_until=end)
        return await ctx.respond("Commande en cours de développement")

    load_slash = component.make_loader()

except Exception as e:
    if os.getenv("ENV") == "DEV":
        print("Error while trying to load mod_punishements.py module with error : ", e)
    else:
        sentry_sdk.capture_exception(e)
