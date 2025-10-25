import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
import datetime
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import time
import asyncio



#Cog to deal with all continuously live updating components
class UpdatesCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising UpdatesCog...")
        self.bot = bot
        
    updates = app_commands.Group(
        name="updates",
        description="Live update commands."
    )



    #Tell the bot to start watching a league.
    @tasks.loop(seconds=5.0)
    async def printer(self):
        pass