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

    leagueID:int = 48 #The ID of the league that this cog cares about.
    currentSeason:int = 2025 #The year of the current season (NOT just the current year! 2025 = 25/26 season etc)

    checkTodayTime = time(hour=0, minute=15) #The time to check today's fixtures
    todayFixtures: list[Fixture] = [] #List of Fixture classes that resets at checkAheadTime each day
    liveFixtures: list[Fixture] = []

    updateGuildList: list[dc.channel.TextChannel] = []

    #Pull all the currently live Fixtures in our league
    async def GetLiveFixtures(self) -> list[Fixture]:

        digest = PullRequest("fixtures", params={"live":"all", "league":self.leagueID, "season":self.currentSeason})

        fixtureList = []
        for fixtureJSON in digest["response"]:
            fixtureList.append(Fixture(fixtureJSON))

        return fixtureList
    
    #This command updates self.liveFixtures with all the new fixtures, and updates already running ones
    async def UpdateLiveFixtures(self, newFixtureList: list[Fixture]) -> None:
        for newFixture in newFixtureList:
            isFixtureNew = True
            #For each fixture, see which fixture in liveFixtures it is:
            for oldFixture in self.liveFixtures:
                if oldFixture.id == newFixture.id:
                    #If we find a matching ID, update the oldFixture with its new details
                    newJsonDict = newFixture.jsonDict
                    oldFixture.UpdateMe(newJsonDict) #Pass the new jsonDict to the old one. Update it.
                    isFixtureNew = False #Not a new Fixture.

            #If it turns out this is an entirely new fixture, then simply add it to the list
            if isFixtureNew == True:
                print(Fore.BLUE + f"Fixture {newFixture.homeTeamName} vs {newFixture.awayTeamName} added to live fixtures list!")
                self.liveFixtures.append(newFixture)

    #When the cog loads this runs
    async def cog_load(self):
        self.LeagueWatcher.start()

    #Live league watcher/update giver
    @tasks.loop(seconds=15)
    async def LeagueWatcher(self) -> None:
        print(Fore.BLUE + "\nRunning LeagueWatcher():")

        #First: get the live fixtures from the league.
        newLiveFixtures: list[Fixture] = await self.GetLiveFixtures()
        print(Fore.BLUE + f"Retrieved {len(newLiveFixtures)} live fixtures.")

        await self.UpdateLiveFixtures(newLiveFixtures)        

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
        newLiveFixtureIDs: list[int] = []
        #The last thing we do is check for finished matches. First we get a list of current and new liveFixture IDs:
        for i in self.liveFixtures:
            currentLiveFixtureIDs.append(i.id)
        for i in newLiveFixtures:
            newLiveFixtureIDs.append(i.id)

        #Now, get a list of all the *CURRENT* live fixture IDs that did not come in the most recent batch of newFixtureIDs:
        endedFixtureIDs = list(set(currentLiveFixtureIDs) - set(newLiveFixtureIDs))
        #All the fixture IDs in this list are fixtures which have *ended*. They won't have shown up in our new PullRequest, so we need to do one final pull to see how they ended.
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
                
    #Before we start watching the league, we need to get everything up to date on the current live fixtures so that we don't spam loads of events as they load in!
    @LeagueWatcher.before_loop
    async def WatchLeagueSetup(self):
        self.liveFixtures = await self.GetLiveFixtures() #Update the liveFixtures list.
        for fixture in self.liveFixtures:
            for event in fixture.eventList:
                #For each event in each fixture, set all events that happened before startup so reported = True
                event.reported = True
        print(Fore.BLUE + f"{len(self.liveFixtures)} live fixtures loaded into memory on startup.")

    #--USER COMMANDS--
    
    @updates.command(name="sendhere", description="Send match updates here")
    async def sendhere(self, interaction):
        guild = interaction.channel
        self.updateGuildList.append(guild)
        
        await interaction.response.send_message("Match updates now being sent here.")
        print(f"{interaction.user} asked for updates in channel {interaction.channel_id}")
