import discord as dc
import discord.interactions as interacts
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import random
import asyncio
import requests
import json
from cogs.silly_cog import SillyCog
from cogs.fbdata_cog import FBDataCog
from cogs.updates_cog import UpdatesCog
import utils.bot_constants as consts 
import utils.secret_constants as sConsts
import utils.dicts as dicts

prefix: str = "!"

class Bot(commands.Bot):
    uptime: datetime = datetime.now(timezone.utc)

    def __init__(self, *, intents: dc.Intents):
        super().__init__(command_prefix=prefix, intents=intents)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=dc.Object(id=sConsts.TEST_GUILD_ID))
        await self.tree.sync(guild=dc.Object(id=sConsts.TEST_GUILD_ID))


intents = dc.Intents.default()
intents.message_content = True
bot = Bot(intents=intents)


#Add our invidiual cogs to the bot's functionality after we turn him on
@bot.event
async def on_ready():
    await bot.add_cog(SillyCog(bot))
    await bot.add_cog(FBDataCog(bot))
    await bot.add_cog(UpdatesCog(bot))
    print(f'We have logged in as {bot.user}.\n')

    

    #These lines automatically sync our command tree to our test guild just so testing is easier 
    testGuild = bot.get_guild(sConsts.TEST_GUILD_ID)
    print(f"Synchronising commands for guild id {testGuild.id}.\n")
    bot.tree.copy_global_to(guild=testGuild)
    cmd_list = await bot.tree.sync(guild=testGuild)
    print(f'{len(cmd_list)} commands were synchronized to guild {testGuild.id}.\n')

#Syncing command to get slash commands to appear in the command list
@bot.command(name="sync")
async def sync(ctx):
    print(f"{ctx.author} synchronising commands for guild id {ctx.guild.id}.\n")
    bot.tree.copy_global_to(guild=ctx.guild)
    cmd_list = await bot.tree.sync(guild=ctx.guild)
    print(f'{len(cmd_list)} commands were synchronized to guild {ctx.guild.id}.\n')

@bot.tree.command(name="ping")
async def ping(interaction):
    await interaction.response.send_message("Fuck off cunt")
    print(f"Pinged by {interaction.user}.\n")

bot.run(sConsts.BOT_KEY)