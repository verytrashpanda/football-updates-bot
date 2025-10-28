from utils.classes import MatchEvent, Fixture
import discord as dc
from colorama import init, Fore, Style
init(autoreset=True)

#Takes a fixture and an event. Generates a report.
async def ReportWriter(fixture: Fixture, event: MatchEvent) -> dc.Embed:
    print(Fore.BLUE + f"EVENT: {event.detail} at {event.normalTime} by {event.player} minutes in {fixture.homeTeamName} vs {fixture.awayTeamName}.")

    reportString: str = ""
    eventString: str = ""
    timeString: str = ""

    scoreCard: str = f"{fixture.homeTeamName} {fixture.homeGoals} - {fixture.awayGoals} {fixture.awayTeamName}"

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
            eventString = f"**GOAL!** {scoreCard}. {event.team} score! Scorer: {event.player}, assist: {event.assist}"
        elif event.detail == "Penalty":
            eventString = f"GOAL! {scoreCard}. {event.team} convert the penalty! Scorer: {event.player}"
        elif event.detail == "Missed Penalty":
            eventString = f"{event.player} misses a penalty for {event.team}. {scoreCard}"
    elif event.type == "subst":
        eventString = f"{event.team} make a sub. {event.player} off, {event.assist} on."
    else:
        eventString = event.detail

    titleString = f"(**{timeString}**) {scoreCard}"

    reportEmbed = dc.Embed()

    reportEmbed.add_field(name=titleString, value=eventString)    

    return reportEmbed