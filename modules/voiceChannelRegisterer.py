import hikari
import tanjun


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_channel_slash_option("channel", "The voice channel to register")
@tanjun.as_slash_command("voiceregister", "Register a voice channel for the user")
async def commandHelp(ctx: tanjun.abc.SlashContext, channel: hikari.InteractionChannel) -> None:
    channelID = channel.id
    print(channelID)
    embed = (
        hikari.Embed(title="The Great Bot", colour=hikari.Colour(0x005087))
            .add_field(name="pouet", value="The Voice Channel has been registered.", inline=False)
    )

    await ctx.respond(embed)


load_slash = component.make_loader()
