import requests
from colorama import init, Fore, Style
init(autoreset=True)

import utils.bot_constants as consts




#The function to make a pull request
def PullRequest(endpoint: str, params: dict) -> dict:
    url = consts.URL_BASE + endpoint
    r = requests.get(url, headers=consts.HEADERS, params=params)
    print(Fore.LIGHTBLACK_EX + f"--> Making GET request to {url}. <--")
    return (r.json())