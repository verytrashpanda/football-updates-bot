import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timezone, timedelta, time
from colorama import init, Fore, Style
init(autoreset=True)

from utils.classes import Fixture, MatchEvent
from utils.pull_request import PullRequest

#Premier League update functionality
class UpdatesCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising UpdatesCog...")
        self.bot = bot
        
    updates = app_commands.Group(
        name="updates",
        description="Live update commands."
    )

    leagueID:int = 39 #The ID of the league that this cog cares about.
    currentSeason:int = 2025 #The year of the current season (NOT just the current year! 2025 = 25/26 season etc)

    updateGuild = 0

    #Returns a list of all of today's Fixtures
    async def GetTodayFixtures(self) -> list[Fixture]:
        today = datetime.now() #Get current date and time
        formattedToday = today.strftime("%Y-%m-%d") # Format date as yyyy-mm-dd
        
        digest = PullRequest("fixtures", {"league" : self.leagueID, "season" : self.currentSeason, "date" : formattedToday})

        fixtureList = []
        for fixtureJson in digest["response"]:
            fixtureList.append(Fixture(fixtureJson))

        return fixtureList

    async def GetLiveFixtures(self) -> list[Fixture]:
        #Pull all the live fixtures in our league
        #digest = PullRequest("fixtures", params={"live":"all", "league":81, "season":2025})
        digest = PullRequest("fixtures", params={"live":"all"})

        fixtureList = []
        for fixtureJson in digest["response"]:
            fixtureList.append(Fixture(fixtureJson))

        return fixtureList


    #When the cog loads this runs
    async def cog_load(self):
        self.liveFixtures = await self.GetLiveFixtures()
        print(f"{len(self.liveFixtures)} live fixtures loaded into memory on startup.")

        self.checkTodayFixtures.start()
        self.LeagueWatcher.start()

        

    checkTodayTime = time(hour=0, minute=15) #The time to check today's fixtures
    todayFixtures: list[Fixture] = [] #List of Fixture classes that resets at checkAheadTime each day
    liveFixtures: list[Fixture] = []

    @tasks.loop(time = checkTodayTime)
    async def checkTodayFixtures(self) -> None:
        self.todayFixtures = [] #Clear the list of fixtures

        self.todayFixtures = await self.GetTodayFixtures()

    #Live league watcher/update giver
    @tasks.loop(seconds=15)
    async def LeagueWatcher(self) -> None:
        try:
            channel = await self.bot.fetch_channel(self.updateGuild)
        except Exception as e:
            print(e)
        print("\nRunning LeagueWatcher():")
        #First: get the live fixtures from the league.
        newLiveFixtures: list[Fixture] = await self.GetLiveFixtures()
        print(f"Retrieved {len(newLiveFixtures)} live fixtures.")

        #Now use them to update all the information about the live fixtures
        for newFixture in newLiveFixtures:
            isFixtureNew = True
            #For each fixture, see which fixture inliveFixtures it is:
            for oldFixture in self.liveFixtures:
                if oldFixture.id == newFixture.id:
                    #If we find a matching ID, update the oldFixture with its new details
                    newJsonDict = newFixture.jsonDict
                    oldFixture.UpdateMe(newJsonDict)
                    isFixtureNew = False

            #If it turns out this is an entirely new fixture, then simply add it to the list
            if isFixtureNew == True:
                print("fixture added to live fixtures list!")
                self.liveFixtures.append(newFixture)
        
        #Print which fixtures are on:
        for i in self.liveFixtures:
            print(f"{i.homeTeamName} vs {i.awayTeamName}")



        #Now we report any new events that have taken place in the matches we're watching.
        for liveFixture in self.liveFixtures:
            newEventList: list[MatchEvent] = liveFixture.ReportEvents()
            for event in newEventList:
                print(f"EVENT: {event.detail} at {event.normalTime} minutes in {liveFixture.homeTeamName} vs {liveFixture.awayTeamName}.")

                try:
                    
                    await channel.send(content=f"EVENT: {event.detail} at {event.normalTime} minutes in {liveFixture.homeTeamName} vs {liveFixture.awayTeamName}.")
                except Exception as e:
                    print(e)


    #--USER COMMANDS--

    @updates.command()
    async def today(self, interaction):
        print(f"performing today() for {interaction.user}.")

        newList = await self.GetTodayFixtures()
        newText = ""

        if len(newList) == 0:
            newText = "No fixtures today."
        else:
            for i in newList:
                newText += f"{i.date}: {i.homeTeam} vs {i.awayTeam} at {i.stadium}.\n"

        embed = dc.Embed()
        embed.add_field(name="Today's fixtures:", value=newText)
        await interaction.response.send_message(embed=embed)

    
    @updates.command(name="sendhere", description="Send match updates here")
    async def sendhere(self, interaction):
        self.updateGuild = interaction.channel_id
        
        
        await interaction.response.send_message("Match updates now being sent here.")
        print(f"{interaction.user} asked for updates in channel {interaction.channel_id}")
