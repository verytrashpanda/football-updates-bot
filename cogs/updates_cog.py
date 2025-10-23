import discord as dc
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import time
import asyncio

updateTimer = 10 #How long between API calls in seconds?

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
    @updates.command(name="watch")
    async def StartWatchLeague(self, interaction, league: str):
        listenChannel = interaction.channel
        await interaction.response.send_message(f"Now watching for updates in {league} in this channel.")
        
        while True:
            await listenChannel.send("fart")
            time.sleep(updateTimer)



    #Make the user's selection for league choice autocomplete
    @StartWatchLeague.autocomplete("league")
    async def LeagueAutocomplete(self, interaction: dc.Interaction, current: str,):
        leagues = list(dicts.updatedLeagues.keys())
        return [
        app_commands.Choice(name=league, value=league)
        for league in leagues if current.lower() in league.lower()
        ]