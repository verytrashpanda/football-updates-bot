import requests
import bot_constants as consts
import secret_constants as sConsts
import json


#We want to use our user-added API key and see what leagues they have access to, which we can do by pulling "competitions".
url = consts.URL_BASE + f"competitions" 
r = requests.get(url, headers=sConsts.HEADERS)
digest = r.json()

#Then we want to map their standard names to their codes, which we use in urls.
updatedLeagues = {}
for comp in digest["competitions"]:
    print(f"Competition: {comp["name"]}. id: {comp["id"]}. Code: {comp["code"]}. Type: {comp["type"]}")

    updatedLeagues[comp["name"]] = comp["code"]
#Now we have a dict of the leagues the bot have access to and their associated codes.




#Dict to include a club's preferred shortName by its ID.
#I don't like to use the football-data.org short names due to error ("Nottingham" instead of "Forest" etc).
properShortNames= {
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