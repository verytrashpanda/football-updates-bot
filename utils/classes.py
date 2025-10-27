from datetime import datetime

from datetime import datetime, timezone

#You pass a ["fixture"] list to this from the API and it assigns/updates itself.
class Fixture:
    def UpdateMe(self, jsonDict):
        isoTime = jsonDict["fixture"]["date"]
        self.date = datetime.fromisoformat(isoTime)

        self.status = jsonDict["fixture"]["status"]["short"]

        self.normalTime = jsonDict["fixture"]["status"]["elapsed"]
        self.extraTime = jsonDict["fixture"]["status"]["extra"]

    def __init__(self, jsonDict):
        self.UpdateMe(jsonDict) 
        self.reportedEvents = 0

        #Initalise the variables which will never change in this class:
        self.id = jsonDict["fixture"]["id"]
        self.homeTeam = jsonDict["teams"]["home"]["name"]
        self.awayTeam = jsonDict["teams"]["away"]["name"]
        self.stadium = jsonDict["fixture"]["venue"]["name"]