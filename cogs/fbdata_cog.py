import discord as dc
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import utils.table_drawing as drawing
import io
import utils.secret_constants as sConsts

urlBase = "https://api.football-data.org/v4/" #Base url to make API requests from
headers = { 'X-Auth-Token': sConsts.API_KEY } #Header with our API token

#This cog will deal with all commands that pull from the football-data.org API for stats and updates.
class FBDataCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising FBDataCog")
        self.bot = bot
        

    fbdata = app_commands.Group(
        name="fbdata",
        description="Football data functionality."
    )

    #Search and print a league table
    @fbdata.command(name="standings", description="Print a league table.", )
    async def Standings(self, interaction, league: str):
        embed = dc.Embed(
            color=dc.Color.from_str(consts.PREM_COLOUR), 
            title=f"{league} Table:"
            )
        embed.timestamp = dc.utils.utcnow()

        #Generate the required URL payload and get the request
        url = urlBase + "competitions/" + dicts.updatedLeagues[league] + "/standings" 
        r = requests.get(url, headers=headers)
        digest = r.json()

        image = drawing.ShowTable(digest)
        
        with io.BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await interaction.response.send_message(file=dc.File(fp=image_binary, filename='image.png'))

        

    #Make the user's selection for league choice autocomplete
    @Standings.autocomplete("league")
    async def LeagueAutocomplete(self, interaction: dc.Interaction, current: str,):
        leagues = list(dicts.updatedLeagues.keys())
        return [
        app_commands.Choice(name=league, value=league)
        for league in leagues if current.lower() in league.lower()
        ]
    
### --------------------- ###

#League Table Image Generation
