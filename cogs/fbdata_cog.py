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
        print("Initialising FBDataCog")
        self.bot = bot
        

    fbdata = app_commands.Group(
        name="fbdata",
        description="Football data functionality."
    )



    #Search and print a league table
    @fbdata.command(name="standings", description="Print the Premier League table.", )
    async def Standings(self, interaction, league_code: str) -> None:
        print(f"Performing standings request for {interaction.user}.")
        cb = await interaction.response.defer(ephemeral=False, thinking=True) #Send thinking response
        int_msg = cb.resource
        
        #Check if the entered code is actually one we can use
        if (league_code not in dicts.updatedLeagues.values()):
            await int_msg.edit(content=f"No league `{league_code}` found. Please enter an accepted league code.")
            print("Unknown/unusable league code entered, exiting command.\n")
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