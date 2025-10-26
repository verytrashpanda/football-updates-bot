import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime
import random
import utils.bot_constants as consts
import utils.secret_constants as sConsts
import utils.dicts as dicts
import time
import asyncio
import json



#Cog to deal with all continuously live updating components
class UpdatesCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising UpdatesCog...")
        self.bot = bot
        
    updates = app_commands.Group(
        name="updates",
        description="Live update commands."
    )

    watching = True 

    #When the bot is turned on, we start "watching" the leagues we're interested in.
    async def cog_load(self):
        if self.watching:
            self.WatchInactives.start()

    url = consts.URL_BASE + "standings"
    headers = sConsts.HEADERS
    params = {
            "league" : 39,
            "season" : 2025
        }

    r = requests.get(url, headers=headers, params=params)
    digest = r.json()

    with open("data.json", "w") as f:
        json.dump(digest, f, indent=2)

    #We define our leagues in two states - active and inactive. While we want to actively watch some leagues for score updates, we inactively want to watch all leagues and store
    #their standings to file to reduce API calls.
    #Inactive leagues have no matches being played, and no matches to be played within the next two hours.
    #Because they have no activity happening, they only need to be updated once a day (essentially to check for points deductions.). 24 calls per day per league.
    #We write these things to file.
    @tasks.loop(hours=24)
    async def WatchInactives(self):
        lastCheckTime = datetime.now()
        print(f"Checking inactive leagues at {lastCheckTime}...")

        

        
