import discord as dc
from discord.ext import commands
from discord import app_commands
import requests
import datetime
import random

#Cog for silly commands
class SillyCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising SillyCog")
        self.bot = bot

    silly = app_commands.Group(
        name="silly",
        description="silly commands"
    )

    @silly.command()
    async def chant(self, interaction):
        await interaction.response.send_message("UP THE FUCKING PALACE!!! <:CrystalPalace:1428728526403534990>:heart::blue_heart:")
        print(f"Performed chant() for {interaction.user}.\n")

    @silly.command()
    async def mushroom_guy(self, interaction):
        await interaction.response.send_message("https://cdn.discordapp.com/attachments/1045941544890400778/1400763076445212762/dancing_fungus-golden.gif")
        print(f"Performed mushroom_guy() for {interaction.user}.\n")

