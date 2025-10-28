#I define a list of leagues we care about here and their associated ID. API-football has 7816 leagues - we do not care about most of them.
updatedLeagues = {
    "Premier League" : 39,
    "Championship" : 40,
    "UEFA Champions League" : 2
}

watchingLeagues = {
    "Premier League" : 39,
}

#dict of preferred (aka correct) aliases for clubs
#I don't like to use the football-data.org shortNames due to error ("Nottingham" instead of "Forest" etc).
#Yes, this is over-engineering and completely overcomplicating things, but I am so anal about the correct names being used for things in football. 
#(depreciated for now)
