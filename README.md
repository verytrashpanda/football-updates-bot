Discord bot that posts standings in the major football leagues. Uses API-football to do so.

The bot's main ideology is keeping API calls as low as possible. The bot watches the leagues it's interested in and then stores their standings internally, spitting them out when asked rather than calling the API every time.

The bot uses a secret_constants.py module not on the repo with API keys and other such things.
Use the secret_constants_examples.py, fill in the values, and rename it to get the bot to work.

The bot is a palace fan and this feature is not optional