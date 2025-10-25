import requests
import utils.bot_constants as consts
import utils.secret_constants as sConsts

#I define a list of leagues we care about here and their associated ID. API-football has 7816 leagues - we do not care about most of them.
updatedLeagues = {
    "Premier League" : 39,
    "Championship" : 40,
    "UEFA Champions League" : 2
}

#dict of preferred (aka correct) aliases for clubs
#I don't like to use the football-data.org shortNames due to error ("Nottingham" instead of "Forest" etc).
#Yes, this is over-engineering and completely overcomplicating things, but I am so anal about the correct names being used for things in football. 
properNames= {
    57 : "Arsenal",
    64 : "Liverpool",
    73 : "Tottenham Hotspur",
    1044 : "Bournemouth",
    65 : "Manchester City",
    354 : "Crystal Palace",
    61 : "Chelsea",
    62 : "Everton",
    71 : "Sunderland",
    66 : "Manchester United",
    67 : "Newcastle",
    397 : "Brighton",
    58 : "Aston Villa",
    63 : "Fulham",
    341 : "Leeds United",
    402 : "Brentford",
    351 : "Nottingham Forest",
    328 : "Burnley",
    563 : "West Ham",
    76 : "Wolves"
}

#Essentially just trying to replace a shortName my properNames alias - if I've not provided a "proper" name then just use the API provided one.
#Overwrought with two inputs but needs to be done this way to keep API requests low.
def GetProperName(id: int, shortName: str) -> str:
    if (id in properNames):
        return properNames[id]
    else:
        return shortName