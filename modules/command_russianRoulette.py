import hikari
import tanjun
import random
import datetime
from datetime import timezone

component = tanjun.Component()


@component.with_slash_command
@tanjun.as_slash_command("roulette", "Joue un round de roulette russe. Si tu perds, tu es TO pendant 30 secondes.")
async def commandRoulette(ctx: tanjun.abc.SlashContext,
                          bot: hikari.GatewayBot = tanjun.injected(type=hikari.GatewayBot)) -> None:
    member = ctx.member
    roulette = ["Clic", "Clic", "Clic", "Clic", "Clic", "Pan"]
    rouletteResult = random.choice(roulette)
    if rouletteResult == "Clic":
        embed = (
            hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0x005087))
                .set_thumbnail("https://i.pinimg.com/736x/b9/1b/36/b91b368ed3c624d9c3d7379a3b3754ee.jpg")
                .add_field(name="*roulements de Tambours...*",
                    value="Bravo, tu as survécu cette fois. Retente ta chance plus tard.",
                    inline=False)
        )
        await ctx.respond(embed)
    elif rouletteResult == "Pan":
        currentDatetime = datetime.datetime.now(timezone.utc)
        newDatetime = currentDatetime + datetime.timedelta(seconds=30)
        await bot.rest.edit_member(guild=ctx.guild_id, user=member, communication_disabled_until=newDatetime)
        if str(ctx.member) == "kono_loki_da":
            embed = (
                hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0x005087))
                .set_thumbnail("https://i.pinimg.com/736x/b9/1b/36/b91b368ed3c624d9c3d7379a3b3754ee.jpg")
                .add_field(name="*roulements de Tambours...*",
                    value="Ben alors Loki, on est naze ? Ben ouais, t'as perdu. Cheh!",
                    inline=False)
            )
        else:
            embed = (
                hikari.Embed(title="Roulette Russe", colour=hikari.Colour(0x005087))
                .set_thumbnail("https://i.pinimg.com/736x/b9/1b/36/b91b368ed3c624d9c3d7379a3b3754ee.jpg")
                .add_field(name="*roulements de Tambours...*",
                    value=f"{member.mention} a perdu au round de roulette russe !",
                    inline=False)
            )
        await ctx.respond(embed)


load_slash = component.make_loader()
