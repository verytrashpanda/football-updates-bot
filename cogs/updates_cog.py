import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timezone, timedelta, time
from colorama import init, Fore, Style
init(autoreset=True)

from utils.classes import Fixture
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

    #Returns a list of all of today's Fixtures
    async def GetTodayFixtures(self) -> list[Fixture]:
        today = datetime.now() #Get current date and time
        formattedToday = today.strftime("%Y-%m-%d") # Format date as yyyy-mm-dd
        
        digest = PullRequest("fixtures", {"league" : 39, "season" : 2025, "date" : formattedToday})

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
        self.todayFixtures = [] #Clear the list of fixtures

        todayFixturesJson = await self.GetTodayFixtures()

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