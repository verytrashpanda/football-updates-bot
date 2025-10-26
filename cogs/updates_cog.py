import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime, timezone, timedelta
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import time
import asyncio
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
    leagueActive = False

    playedCodes = ["1H", "HT", "2H", "ET", "BT", "P"]

    todayFixtures = [] #List of the fixtures from today to next week. Only actively updated when the league is ACTIVE.
    liveFixtures = []

    #This function gets every single game being played from today until next week.
    async def GetTodayFixtures(self) -> dict:
        today = datetime.now() #Get current date and time
        formattedToday = today.strftime("%Y-%m-%d") # Format date as yyyy-mm-dd
        nextWeek = today + timedelta(weeks=1)
        formattedNextWeek = nextWeek.strftime("%Y-%m-%d")
        
        digest = PullRequest("fixtures", {"league" : 39, "season" : 2025, "date" : formattedToday})
        return digest["response"]
    
    async def cog_load(self): #On cog load
        self.nextWeekFixtures = self.GetNextWeek()
        self.WakeManager.start()
        self.SlowChecker.start()

    #Loop runs and manages if the league is awake or asleep.
    @tasks.loop(minutes=1)
    async def WakeManager(self):
        if self.leagueActive == False:
            try:
                dateISO = self.todayFixtures[0]["fixture"]["date"]
                nextMatchTime = datetime.fromisoformat(dateISO)
                timeUntilNextMatch = nextMatchTime - datetime.now(timezone.utc)

                #If the next match is 1 minute or less away (or has already started)...
                if timeUntilNextMatch.total_seconds() <= 65:
                    print(Fore.BLUE + "!!! League is ACTIVE !!! \n")
                    self.leagueActive = True
            except:
                print("No fixtures today.")

        if self.leagueActive == True:
            #If no matches are live anymore, go to sleep
            if len(self.liveFixtures) == 0:
                print(Fore.BLUE + "!!! League is INACTIVE !!! \n")
                self.leagueActive = False

#This guy's job is to keep the Fixture classes in the list updated.
@tasks.loop(minutes=1)
async def FixtureHandler(self):
    if self.leagueActive == False:
        return
    
    #Get our fixture list from the site.
    requestedList = self.GetTodayFixtures()

    #For each entry in the fixture list 



#Always runs in the background. Only goes forth if the league is inactive. Keeps nextWeekFixtures updated long-term.
@tasks.loop(hours=2)
async def SlowChecker(self):
    if self.leagueActive == True:
        return

    self.todayFixtures = self.GetTodayFixtures()