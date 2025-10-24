from PIL import Image, ImageDraw, ImageFont, ImageText, ImageFilter
import requests
import utils.bot_constants as consts 
import utils.dicts as dicts
from io import BytesIO
import os

class Team:
    def __init__(self, position = 0, name = "", points = 0 , logo = ""):
        self.position = position
        self.name = name
        self.points = points
        self.logo = logo

#Takes a standings digest, spits out a league table image.
async def GetTableImage(digest) -> Image:
    #List of Team classes
    cellList = []

    #Creating however many Teams we need and adding them to cellList
    for club in digest["standings"][0]["table"]:
        newClub = Team()

        newClub.position = club["position"]
        newClub.name = dicts.GetProperName(club["team"]["id"], club["team"]["shortName"])
        newClub.points = club["points"]
        newClub.logoLink = club["team"]["crest"]

        cellList.append(newClub)

    cellHeight = 40
    halfCellHeight = round(cellHeight / 2)
    tableHeight = (len(cellList) + 1) * cellHeight

    #Defining our font
    mainFont = ImageFont.truetype("OCRAEXT.TTF", cellHeight / 2)
    headerFont = ImageFont.truetype("OCRAEXT.TTF", cellHeight / 2)

    #Defining our header
    header = ["Pos", "Team", "", "Pts."]
    headerDimensions = [cellHeight, cellHeight, 300, cellHeight]
    tableWidth = sum(headerDimensions) #The length of all our header components, obviously

    tableImage = Image.new(mode="RGB", size=(tableWidth,tableHeight), color="#1a1a1a")
    print(f"Creating a league table image with {len(cellList)} rows ({tableWidth}x{tableHeight}).")
    draw = ImageDraw.Draw(tableImage)

    xPos = 0
    i = 0
    #Draw the header
    for title in header:
        draw.text([xPos, 0 + halfCellHeight], title, font=headerFont, anchor="lm")
        draw.line(([xPos, 0],[xPos, tableHeight]), width=1, fill="grey")
        xPos += headerDimensions[i]
        
        i+=1
    draw.line(([0, cellHeight], [tableWidth, cellHeight]), width = 2, fill="white")

    yPos = 0
    for cell in cellList:
        xPos = 0 #reset to the left of the image each time
        yPos += cellHeight #move down a cell

        #Place the position in the image
        draw.text([xPos + halfCellHeight, yPos+halfCellHeight], str(cell.position),font=mainFont, anchor="mm")
        xPos += headerDimensions[0]

        #Place the logo in the image
        logoOffset = 10
        logoResponse = requests.get(cell.logoLink)
        logo = Image.open(BytesIO(logoResponse.content)).convert("RGBA")

        thumbnailDimension = cellHeight - logoOffset
        logo.thumbnail([thumbnailDimension, thumbnailDimension])

        tableImage.paste(logo, [xPos + round(logoOffset/2), yPos + round(logoOffset/2)], logo)

        xPos += headerDimensions[1]

        #Place the team name in the image
        draw.text([xPos + 10, yPos + halfCellHeight], cell.name, font=mainFont, anchor="lm")
        xPos += headerDimensions[2]

        #Place the points in the image
        draw.text([xPos+halfCellHeight, yPos + halfCellHeight], str(cell.points), font=mainFont, anchor="mm")
        
        #Draw the cell line
        draw.line(([0, yPos], [tableWidth, yPos]), width=1, fill="white")
    
    return tableImage