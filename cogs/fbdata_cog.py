import discord as dc
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import random
import json
import utils.bot_constants as consts
import utils.dicts as dicts
import utils.table_drawing as drawing
from io import BytesIO
import utils.secret_constants as sConsts
from PIL import Image, ImageDraw, ImageFont, ImageText, ImageFilter

urlBase = consts.URL_BASE #Base url to make API requests from
headers = sConsts.HEADERS #Header with our API token

#This cog will deal with all commands that pull from the football-data.org API for stats and updates.
class FBDataCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising FBDataCog...")
        self.bot = bot
        

    fbdata = app_commands.Group(
        name="fbdata",
        description="Football data functionality."
    )



    #Search and print a league table
    @fbdata.command(name="standings", description="Print a league table.", )
    async def Standings(self, interaction, league_code: str) -> None:
        print(f"Performing Standings() request for {interaction.user}.")
        cb = await interaction.response.defer(ephemeral=False, thinking=True) #Send thinking response
        int_msg = cb.resource

        league_code = league_code.upper() #codes are all uppercase
        
        #Check if the entered code is actually one we can use
        if (league_code not in dicts.updatedLeagues.values()):
            await int_msg.edit(content=f"No league `{league_code}` found. Use /fbdata available_leagues to see league codes.")
            print(f"Unknown/unusable league code {league_code} entered, exiting command.\n")
            return None

        #Generate the required URL payload and get the request
        url = urlBase + f"competitions/{league_code}/standings" 
        r = requests.get(url, headers=headers)
        digest = r.json()

        image = await drawing.GetTableImage(digest) #Get table image

        #Add it as our embed to our message
        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            await int_msg.edit(attachments=[dc.File(fp=image_binary, filename='image.png')])
            print(f"Posted {league_code} table for {interaction.user}.\n")

    #Show the user available leagues
    @fbdata.command(name="available_leagues", description="Get a list of available leagues.")
    async def PrintAvailableLeagues(self, interaction) -> None:
        print(f"Performing PrintAvailableLeagues() request for {interaction.user}.")
        cb = await interaction.response.defer(ephemeral=True, thinking=True) #Send thinking response
        int_msg = cb.resource

        responseContent = "The following leagues (and associated codes) are available:\n"
        for name, code in dicts.updatedLeagues.items():
            responseContent += f"* {name} ({code})\n"
        
        embed = dc.Embed(colour=dc.Colour.from_str(consts.PREM_COLOUR))
        embed.add_field(name="Available Leagues", value=responseContent)

        await int_msg.edit(embed=embed)
        print(f"PrintAvailableLeagues() completed for {interaction.user}.\n")

