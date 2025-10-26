import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime, timezone
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import time
import asyncio
import json
from utils.pull_request import PullRequest
from colorama import init, Fore, Style
init(autoreset=True)

#For now, we only actively update with Premier League functionality.

#Below we define two states: "Live" and "Inactive".

#Cog to deal with all continuously live updating components
class UpdatesCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising UpdatesCog...")
        self.bot = bot
        
    updates = app_commands.Group(
        name="updates",
        description="Live update commands."
    )

    #Is the league "active" right now?
    leagueActive = False

    #Current standings
    standings = {}

    #These lists contain fixture dictionaries. They're class attributes so they can be shared across functions :)
    nextMatches: list[dict] = [] #List of every live match. Keep in mind this is only ever updated while the league is *INACTIVE* and processed in batches of 10.
    liveMatches: list[dict] = [] #List of every live match. 

    #Function that pulls the league table and saves it to datacache/Premier_League.json
    async def SaveTable(self):
        lastCheckTime = datetime.now(timezone.utc)
        params = {"league" : 39, "season" : 2025}
        digest = PullRequest("standings", params=params)
        digest["lastChecked"] = str(lastCheckTime)

        #We also want access to this locally rather than needing to get it from file every time.
        self.standings = digest

        #Save to file
        fileName = "Premier_League"
        filePath = f"datacache/{fileName}.json"
        with open(filePath, "w") as f:
            json.dump(digest, f, indent=2) #Write to file
        print(f"Wrote {league_name} table to {filePath} at {lastCheckTime}.")

    #When the cog is loaded:
    async def cog_load(self):
        #The very first thing we do is check if any prem games are being played *right now*.
        liveCheckDigest = PullRequest("fixtures", {"live":"all", "league":39})
        if liveCheckDigest["results"] != 0: 
            #If there are games on right now then set the league to active
            self.leagueActive = True

        #Now we want to get the next 10 prem matches and put them in a list.
        nextTenDigest = PullRequest("fixtures", {"league":premID, "next":10})
        self.nextMatches = nextTenDigest["response"]

        #Start the inactive and active watchers, which run always.
        self.WatchInactive.start()
        self.WatchActive.start()
        
        #Start the watch handler.
        self.WatchHandler.start()
        
    #The main function that controls whether leagueActive is true or not.
    #If there's a match in <5 minutes, wake up and set the league to active.
    #When we no longer pull live matches, go back to sleep.
    @tasks.loop(minutes=1)
    async def WatchHandler(self) -> None:
        print(Fore.BLUE + "WatchHandler() running.")
        #If the league is inactive:
        if self.leagueActive == False:
            dateISO = self.nextMatches[0]["fixture"]["date"]
            nextMatchTime = datetime.fromisoformat(nextMatchISO)
            timeUntilNextMatch = nextMatchTime - datetime.now(timezone.utc)
            
            #If the next match is 5 minutes or less away (or has already started)...
            if timeUntilNextMatch.total_seconds() <= 300:
                self.leagueActive = True #Wake up the league
                print(Fore.Blue + "!!! League is now ACTIVE. !!!")

        if self.leagueActive == True:
            #If the league is active, every minute we're going to record every single live match and the table.
            self.SaveTable() 
            digest = PullRequest("fixtures", params={"league":39, "season":2025, "live":"all"})
            self.liveMatches = digest["response"]

            #If we don't pull any matches on our live match pull, then we can send the league back to sleep.
            if len(digest["response"] == 0):
                digest = PullRequest("fixtures", params={"league":39, "season":2025, "next":10})
                self.nextMatches = digest["response"] #Update nextMatches with the next 10 matches.

                self.leagueActive = False #Set the league to inactive.

    @tasks.loop(seconds=30)
    async def KickoffManager(self):
        if self.leagueActive == False:
            return
        
        #While the league is active, iterate through all the items in a copy of the nextMatches list
        for entry in self.nextMatches[:]: #A shallow copy of the list
            dateISO = entry["fixture"]["date"]
            nextMatchTime = datetime.fromisoformat(nextMatchISO)
            timeUntilNextMatch = nextMatchTime - datetime.now(timezone.utc)
        

    #The function to watch a specific match and report on it. Called about 500 times per match.
    #Ideally called for the first time about 5 minutes before a match starts.
    @tasks.loop(seconds=20)
    async def WatchMatchEvents(self, id: int) -> None:
        #Pull all the events that have happened in the match.
        pass
        
        


    #Watch the league when it's inactive and update the table and next fixtures. Runs ALWAYS.
    @tasks.loop(hours=6)
    async def WatchInactive(self) -> None:
        if self.leagueActive == True: 
            return # Skip iteration if league is active.

        self.SaveTable() #Save the table with its lastChecked timestamp.

        #Pull and record the next ten fixtures
        nextTenDigest = PullRequest("fixtures", {"league":premID, "next":10})
        self.nextMatches = nextTenDigest["response"]

    #Watch the league while it's ACTIVE. Over a match this will be called ~120 times.
    #Over, for example, a 4 match Premier League Saturday, this will be called about 500 times.
    #Two API pulls per call.
    @tasks.loop(seconds=60)
    async def WatchActive(self, league_name: str) -> None:
        if league.Active == False:
            return #Skip iteration if league is inactive 

        self.SaveTable() #If active, pull and save the table.
        
        #Then pull and record the live fixtures:
        digest = PullRequest("fixtures", params={"league":39, "season":2025, "live":all})
        self.liveMatches = digest["response"]
        


