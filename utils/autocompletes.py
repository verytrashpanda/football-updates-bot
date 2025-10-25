import utils.dicts as dicts
import discord as dc
from discord import app_commands

#Autocomplete function for league names
async def LeagueNameAutocomplete(interaction: dc.Interaction, current: str) -> list[app_commands.Choice["str"]]:
    names = list(dicts.updatedLeagues.keys())
    return [
    app_commands.Choice(name=name, value=name)
    for name in names if current.lower() in name.lower()
]