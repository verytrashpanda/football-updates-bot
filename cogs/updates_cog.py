import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime, timezone, timedelta, time
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import asyncio
from utils.classes import Fixture
import json
from utils.pull_request import PullRequest
from colorama import init, Fore, Style
init(autoreset=True)

#Premier League update functionality
class UpdatesCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising UpdatesCog...")
        self.bot = bot
        
    updates = app_commands.Group(
        name="updates",
        description="Live update commands."
    )

    async def GetTodayFixtures(self) -> list:
        today = datetime.now() #Get current date and time
        formattedToday = today.strftime("%Y-%m-%d") # Format date as yyyy-mm-dd

        testToday = "2025-10-26"
        
        digest = PullRequest("fixtures", {"league" : 39, "season" : 2025, "date" : testToday})

        fixtureList = []
        for fixture in digest["response"]:
            fixtureList.append(Fixture(fixture))

        return fixtureList

    async def cog_load(self):
        self.checkTodayFixtures.start()

    checkAheadTime = time(hour=0, minute=15) #The time to check today's fixtures
    todayFixtures: list = [] #List of Fixture classes that resets at checkAheadTime each day


    @tasks.loop(time = checkAheadTime)
    async def checkTodayFixtures(self) -> None:
        self.todayFixtures = [] #Clear the list of fixtures (unnecessary but just in case)

        todayFixturesJson = await self.GetTodayFixtures()

    @updates.command()
    async def test(self, interaction):
        newList = await self.GetTodayFixtures()

        for i in newList:
            print(i)