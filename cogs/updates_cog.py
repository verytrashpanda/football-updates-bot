import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timezone, timedelta, time
from colorama import init, Fore, Style
init(autoreset=True)

from utils.classes import Fixture, MatchEvent
from utils.pull_request import PullRequest
from utils.functions import GetReportString

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

    checkTodayTime = time(hour=0, minute=15) #The time to check today's fixtures
    todayFixtures: list[Fixture] = [] #List of Fixture classes that resets at checkAheadTime each day
    liveFixtures: list[Fixture] = []

    updateGuildList: list[dc.channel.TextChannel] = []

    async def GetLiveFixtures(self) -> list[Fixture]:
        #Pull all the live fixtures in our league
        digest = PullRequest("fixtures", params={"live":"all", "league":48, "season":2025})
        #digest = PullRequest("fixtures", params={"live":"all"})

        fixtureList = []
        for fixtureJson in digest["response"]:
            fixtureList.append(Fixture(fixtureJson))

        return fixtureList
    
   



    #When the cog loads this runs
    async def cog_load(self):
        self.liveFixtures = await self.GetLiveFixtures()
        for fixture in self.liveFixtures:
            for event in fixture.eventList:
                event.reported = True #Set all events that happened before startup to reported so we don't re-report them
        print(Fore.BLUE + f"{len(self.liveFixtures)} live fixtures loaded into memory on startup.")

        self.LeagueWatcher.start()

        



    @tasks.loop(time = checkTodayTime)
    async def checkTodayFixtures(self) -> None:
        self.todayFixtures = [] #Clear the list of fixtures

        self.todayFixtures = await self.GetTodayFixtures()



    #Live league watcher/update giver
    @tasks.loop(seconds=15)
    async def LeagueWatcher(self) -> None:
        
        newFixtureIDs: list[int] = []

        print(Fore.BLUE + "\nRunning LeagueWatcher():")
        #First: get the live fixtures from the league.
        newLiveFixtures: list[Fixture] = await self.GetLiveFixtures()
        print(Fore.BLUE + f"Retrieved {len(newLiveFixtures)} live fixtures.")

        #Now use them to update all the information about the live fixtures
        for newFixture in newLiveFixtures:
            newFixtureIDs.append(newFixture.id) #Add its ID to a list
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
                print(Fore.BLUE + f"Fixture {newFixture.homeTeamName} vs {newFixture.awayTeamName} added to live fixtures list!")
                self.liveFixtures.append(newFixture)

        #Now we report any new events that have taken place in the matches we're watching.
        for liveFixture in self.liveFixtures:
            newEventList: list[MatchEvent] = liveFixture.ReportEvents()
            for event in newEventList:
                print(Fore.BLUE + f"EVENT: {event.detail} at {event.normalTime} by {event.player} minutes in {liveFixture.homeTeamName} vs {liveFixture.awayTeamName}.")

                sendString = GetReportString(event)

                for textChannel in self.updateGuildList:
                    try:
                        await textChannel.send(content=sendString)
                    except:
                        pass

        currentLiveFixtureIDs: list[int] = []
        #The last thing we do is check for finished matches. First we get a list of current liveFixture IDs:
        for i in self.liveFixtures:
            currentLiveFixtureIDs.append(i.id)
        #Now, get a list of all the *CURRENT* live fixture IDs that did not come in the most recent batch of newFixtureIDs:
        endedFixtureIDs = list(set(currentLiveFixtureIDs) - set(newFixtureIDs))
        #All the fixture IDs in this list are fixtures which have *ended*. They won't have shown up in our new live list, so we need to do one final pull to see how they ended.
        for id in endedFixtureIDs:
            endedFixtureJSON = PullRequest("fixtures", params={"id":id})
            endedFixture = Fixture(endedFixtureJSON["response"][0])

            matchEndString = f"Final whistle: {endedFixture.homeTeamName} {endedFixture.homeGoals} - {endedFixture.awayGoals} {endedFixture.awayTeamName}"
            print(Fore.BLUE + f"MATCH END: {endedFixture.homeTeamName} vs {endedFixture.awayTeamName}")
            for textChannel in self.updateGuildList:
                    try:
                        await textChannel.send(content=matchEndString)
                    except:
                        pass
            
            #And now we need to remove this fixture from the liveFixture list.
            for fixture in self.liveFixtures:
                if fixture.id == id:
                    self.liveFixtures.remove(fixture)
                    return



    #--USER COMMANDS--
    
    @updates.command(name="sendhere", description="Send match updates here")
    async def sendhere(self, interaction):
        guild = interaction.channel
        self.updateGuildList.append(guild)
        
        await interaction.response.send_message("Match updates now being sent here.")
        print(f"{interaction.user} asked for updates in channel {interaction.channel_id}")
