from datetime import datetime

#You pass a ["team"] dict to this from afrom the api to get a class
#class Team:
    #def __init__(self, jsonDict):
        #self.id: int = jsonDict["id"]
        #self.name: str = jsonDict["name"]
        #self.code: str = jsonDict["team"]["code"]
        #self.founded: int = jsonDict["team"]["founded"]
        #self.national: bool = jsonDict["team"]["national"]
        #self.logo: str = jsonDict["logo"]

        #self.venueName: str = jsonDict["venue"]["name"]
        #self.venueCapacity: int = jsonDict["venue"]["capacity"]

#Defines a single event in a match.
class MatchEvent:
    def __init__(self, jsonDict):
        self.reported: bool = False #All events initiate unreported.
        self.normalTime: int = jsonDict["time"]["elapsed"]
        self.extraTime: int = jsonDict["time"]["extra"]

        self.team: str = jsonDict["team"]["name"]

        self.player: str = jsonDict["player"]["name"]

        self.assist: str = jsonDict["player"]["name"]

        self.type: str = jsonDict["type"]
        self.detail: str = jsonDict["detail"]
        self.comment: str = jsonDict["comments"]

#You pass a ["fixture"] dict to this from the API and it assigns/updates itself.
class Fixture:
    def __init__(self, jsonDict):
        self.UpdateMe(jsonDict) #Initialise all the variables that can change
        self.eventList = []

        #Initalise the variables which will never change in this class:
        self.id:int = jsonDict["fixture"]["id"]
        self.referee:str = jsonDict["fixture"]["referee"]
        self.homeTeam:str = jsonDict["teams"]["home"]["name"]
        self.homeTeamLogo:str = jsonDict["teams"]["home"]["logo"]
        self.homeTeamID:int = jsonDict["teams"]["home"]["id"]
        self.awayTeam:str = jsonDict["teams"]["away"]["name"]
        self.awayTeamLogo:str = jsonDict["teams"]["away"]["logo"]
        self.awayTeamID:int = jsonDict["teams"]["away"]["id"]

    def UpdateMe(self, jsonDict) -> None: #This function updates the attributes that should change
        #Date - can change if a match is rescheduled, but mostly shouldn't on the day.
        isoTime: str = jsonDict["fixture"]["date"] 
        self.date: datetime = datetime.fromisoformat(isoTime) 

        #Short and long status information
        self.statusCode:str = jsonDict["fixture"]["status"]["short"]
        self.statusLong:str = jsonDict["fixture"]["status"]["long"]

        #Match information
        self.normalTime:int = jsonDict["fixture"]["status"]["elapsed"]
        self.extraTime:int = jsonDict["fixture"]["status"]["extra"]
        self.homeGoals:int = jsonDict["goals"]["home"]
        self.awayGoals:int = jsonDict["goals"]["away"]

        #Updating the list of events
        try: #If an ["events"] list exists:
            if len(jsonDict["events"]) > len(self.eventList): #If, since last time we checked, a new event has occured
                startIndex = len(self.eventList)
                endIndex = len(jsonDict["events"])
                for i in range(startIndex, endIndex): #iterate through the new events
                    newEvent = MatchEvent(jsonDict["events"][i]) #Create a MatchEvent class from the dictionary
                    self.eventList.append(newEvent) #Add it to our maintained list
        except:
            print("When updating a fixture, it had no events list.\n")

    #Ask the class to check its events list, and return an ordered list of all MatchEvents with reported == False, then set them to True 
    def ReportEvents(self) -> list[MatchEvent]:
        newEvents = []

        for event in self.eventList:
            if event.reported == False:
                newEvents.append(event)
                event.reported == True
        
        return newEvents




