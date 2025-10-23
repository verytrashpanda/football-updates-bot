#Dict of the leagues I have access to and their associated codes
updatedLeagues = {
    "Premier League" : "PL",
    "Champions League" : "CL",
    "Primeira Liga" : "PPL",
    "Eredivisie" : "DED",
    "Bundesliga" : "BL1",
    "Ligue 1" : "FL1",
    "Serie A (IT)" : "SA",
    "La Liga" : "PD",
    "Championship" : "ELC",
    "Serie A (BR)" : "BSA"
}

#Dict about clubs, football-data.org ID is their key and the value is a list of information about them. The IDs should never change as they're set by the API.
#I don't like to use the football-data.org short names for example due to error ("Nottingham" instead of "Forest").
clubInfo = {
    57 : "Arsenal FC",
    64 : "Liverpool FC",
    73 : "Tottenham Hotspur FC",
    1044 : "AFC Bournemouth",
    65 : "Manchester City FC",
    354 : "Crystal Palace FC",
    61 : "Chelsea FC",
    62 : "Everton FC",
    71 : "Sunderland AFC",
    66 : "Manchester United FC",
    67 : "Newcastle United FC",
    397 : "Brighton & Hove Albion FC",
    58 : "Aston Villa FC",
    63 : "Fulham FC",
    341 : "Leeds United FC",
    402 : "Brentford FC",
    351 : "Nottingham Forest FC",
    328 : "Burnley FC",
    563 : "West Ham United FC",
    76 : "Wolverhampton Wanderers FC"
}