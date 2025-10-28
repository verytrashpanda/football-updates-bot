import utils.secret_constants as sConsts
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PREM_COLOUR = "#00ff85"
URL_BASE = "https://v3.football.api-sports.io/" #Base url we get all requests from

#Secret stuff
HEADERS = {
  'x-rapidapi-key': sConsts.API_KEY,
  'x-rapidapi-host': 'v3.football.api-sports.io'
}
BOT_KEY = sConsts.BOT_KEY
TEST_GUILD_ID = sConsts.TEST_GUILD_ID
API_KEY = sConsts.TEST_GUILD_ID
