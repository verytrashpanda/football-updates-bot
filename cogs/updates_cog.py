import discord as dc
from discord.ext import commands, tasks
from discord import app_commands
import requests
from datetime import datetime, timezone, timedelta
import random
import utils.bot_constants as consts
import utils.dicts as dicts
import time
import asyncio
import json
from utils.pull_request import PullRequest
from colorama import init, Fore, Style
init(autoreset=True)

#Premier League update functionality
class UpdatesCog(commands.Cog):
    def __init__(self, bot):
        print("Initialising UpdatesCog...")
        self.bot = bot
        
    updates = app_commands.Group(
        name="updates",
        description="Live update commands."
    )
    