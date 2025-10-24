Discord bot that posts standings in the major football leagues. 

To use this bot you'll need (for now) to supply your own API key to football-data.org. Then you'll need to add a secret_constants.py folder in the utils folder that looks something like this:

TEST_GUILD_ID = (ID of your test discord server)
BOT_KEY = (your bot key)
API_KEY = (your API key for football-data.org)
HEADERS = { 'X-Auth-Token': API_KEY }

The bot is a palace fan and that feature isn't optional
