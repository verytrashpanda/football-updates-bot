import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import time
import asyncio
import json
from utils.pull_request import PullRequest



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
            self.WatchActiveLeagues.start()

    #This is the function watch any league that does not have a match in the next 2 hours.
    @tasks.loop(hours=24)
    async def WatchInactives(self) -> None:
        lastCheckTime = datetime.now()
        print(f"Checking inactive leagues at {lastCheckTime}...")

    #This is our function to update league tables *actively*. We only use this when a match is BEING PLAYED actively - over a game this will be called ~120 times.
    #Over, for example, a 4 match Premier League Saturday, this will be called about 500 times.
    @tasks.loop(seconds=60)
    async def WatchActiveLeagues(self) -> None:
        lastCheckTime = datetime.now()
        print(f"Checking ACTIVE league tables at {lastCheckTime}.")

        for leagueName, id in dicts.watchingLeagues.items():
            params = {"league" : id, "season" : 2025}
            digest = PullRequest("standings", params=params)

            digest["lastChecked"] = str(lastCheckTime)

            fileName = leagueName.replace(" ", "_")
            with open(f"datacache/{fileName}.json", "w") as f:
                json.dump(digest, f, indent=2)