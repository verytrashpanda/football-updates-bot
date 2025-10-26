import utils.bot_constants as consts
import requests
from colorama import init, Fore, Style

init(autoreset=True)



#The function to make a pull request
def PullRequest(endpoint: str, params: dict) -> dict:
    url = consts.URL_BASE + endpoint
    r = requests.get(url, headers=consts.HEADERS, params=params)
    print(Fore.LIGHTBLACK_EX + "--> Making GET request to {url}. <--")
    return (r.json())