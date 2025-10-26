import utils.bot_constants as consts
import requests

#The function to make a pull request
def PullRequest(endpoint: str, params: dict) -> dict:
    url = consts.URL_BASE + endpoint
    r = requests.get(url, headers=consts.HEADERS, params=params)
    return (r.json())
