import hikari
import tanjun
import nacl.utils
from nacl.public import PrivateKey, Box


component = tanjun.Component()
'''
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

print("Public Key: ", public_key, "\nPrivate Key: ", private_key)
'''


@component.with_slash_command
@tanjun.as_slash_command("help", "Display the help for the bot")
async def commandHelp(ctx: tanjun.abc.SlashContext) -> None:
    translateCMD = "/translate will translate a text you input to the targeted language.\n/filetranslate will translate a file you input to the targeted language."
    languagesCMD = "/languages will display all languages available for translation."
    domainsCMD = "/domains will display all the specific domains that can be used. Please note that some domains aren't available to all languages."
    embed = (
        hikari.Embed(title="Help & Informations", colour=hikari.Colour(0x005087), description="Please note that there is a 20k characters limit monthly.")
            .set_footer(text="Powered by SYSTRAN Translate",
                        icon="https://translate.systran.net/images/favicons/apple-touch-icon.png")
            .add_field(name="Translation command.", value=translateCMD, inline=False)
            .add_field(name="Languages command.", value=languagesCMD, inline=False)
            .add_field(name="Domains command.", value=domainsCMD, inline=False)
            .add_field(name="Permissions", value="The bot needs the following permissions to work properly:\n- Send Messages\n- Read Message History", inline=False)
            .add_field(name="Support", value="If you need help, please join the support server: https://discord.gg/2Z7Y4Z4", inline=False)
    )

    await ctx.respond(embed)


load_slash = component.make_loader()
