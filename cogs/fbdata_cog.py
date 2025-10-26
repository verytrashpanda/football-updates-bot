import discord as dc
from discord.ext import commands
from discord import app_commands
import requests
from datetime import datetime
import random
import json
import os
import utils.bot_constants as consts
import utils.dicts as dicts
import utils.table_drawing as drawing
from utils.pull_request import PullRequest
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageText, ImageFilter
from utils.autocompletes import LeagueNameAutocomplete

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
    @fbdata.command(name="standings", description="Print a league table.")
    @app_commands.autocomplete(league_name=LeagueNameAutocomplete)
    async def Standings(self, interaction, league_name: str) -> None:
        print(f"Performing Standings() request for {interaction.user}.")
        cb = await interaction.response.defer(ephemeral=False, thinking=True) #Send thinking response
        int_msg = cb.resource

        #Check if the entered name is actually one we can use
        if (league_name not in dicts.updatedLeagues.keys()):
            await int_msg.edit(content=f"No league `{league_name}` found. Use /data available_leagues to see league codes.")
            print(f"Unknown/unusable league code {league_name} entered, exiting command.\n")
            return None

        #Check if we already have a standings json file
        filepathCheck = f"datacache/{league_name.replace(" ", "_")}.json"
        if os.path.exists(filepathCheck):
            #If we do, just retrieve it and use it as our digest
            with open(filepathCheck, "r") as f:
                digest = json.load(f)
            print(f"Retrieving .json from {filepathCheck}")
        else:
            #Generate a new digest with a pull request
            params = {
                "league" : dicts.updatedLeagues[league_name],
                "season" : 2025
            }
            digest = PullRequest("standings", params)
            digest["lastChecked"] = str(datetime.now())

        image = await drawing.GetTableImage(digest) #Get table image

        #Add it as our embed to our message
        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)

            #Create a discord.File
            imageFile = dc.File(fp=image_binary, filename='image.png')

            #Create an embed
            timestamp = datetime.strptime(digest["lastChecked"], "%Y-%m-%d %H:%M:%S.%f")
            embed = dc.Embed(colour=dc.Colour.from_str(consts.PREM_COLOUR), timestamp=timestamp)
            embed.set_image(url="attachment://image.png")
            embed.set_footer(text="Last updated at:")

            #Edit message
            await int_msg.edit(embed=embed, attachments=[imageFile])

        print(f"Posted {league_name} table for {interaction.user}.\n")

        

    #Show the user available leagues
    @fbdata.command(name="available_leagues", description="Get a list of available leagues.")
    async def PrintAvailableLeagues(self, interaction) -> None:
        print(f"Performing PrintAvailableLeagues() request for {interaction.user}.")
        cb = await interaction.response.defer(ephemeral=True, thinking=True) #Send thinking response
        int_msg = cb.resource

        #Look at our list of leagues we care about and print out each name
        responseContent = "The following leagues are available:\n"
        for name in dicts.updatedLeagues.values():
            responseContent += f"* {name}\n"
        
        embed = dc.Embed(colour=dc.Colour.from_str(consts.PREM_COLOUR))
        embed.add_field(name="Available Leagues", value=responseContent)

        await int_msg.edit(embed=embed)
        print(f"PrintAvailableLeagues() completed for {interaction.user}.\n")

