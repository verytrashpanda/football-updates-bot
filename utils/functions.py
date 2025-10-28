from utils.classes import MatchEvent


#Function that formats reports to be sent. 
def GetReportString(event: MatchEvent) -> str:
    reportString: str = ""
    eventString: str = ""
    timeString: str = ""

    if event.extraTime == None:
        timeString = f"{event.normalTime}'"
    else:
        timeString = f"{event.normalTime}+{event.extraTime}'"

    if event.type == "Card":
        if event.comment == None:
            eventString = f"{event.player} of {event.team} shown a {event.detail}."
        else:
            eventString = f"{event.player} of {event.team} shown a {event.detail} for {event.comment.lower()}."
    elif event.type == "Goal":
        if event.detail == "Normal Goal":
            eventString = f"GOAL! {event.team} score! Scorer: {event.player}, assist: {event.assist}"
        elif event.detail == "Penalty":
            eventString = f"GOAL! {event.team} convert the penalty! Scorer: {event.player}"
        elif event.detail == "Missed Penalty":
            eventString = f"{event.player} misses a penalty."
    elif event.type == "subst":
        eventString = f"{event.team} make a sub. {event.player} off, {event.assist} on."
    else:
        eventString = event.detail

    reportString = f"{timeString}: {eventString}"
    return reportString