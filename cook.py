import csv
import re
import os

def parseDraft(decklistDict, lines, nameDict):
    seenPoints = False
    seenNumber = False
    seenName = False
    number = 0

    pointsPattern = re.compile("Points")
    numberPattern = re.compile("[0-9]+")
    pattern = re.compile("([0-9]+(-[0-9]+)+)")
    endPattern = re.compile("Displaying")

    for line in lines:
        if endPattern.match(line):
            return

        if pointsPattern.match(line):
            seenPoints = True

        if not seenPoints:
            continue

        if numberPattern.match(line):
            seenNumber = True
            number = int(line)
        elif seenNumber and not seenName:
            name = line.split('<')[0]
            nameDict[number] = name
            seenName = True
        elif seenNumber and seenName:
            if(len(line.split("\t")) <= 1):
                continue

            standing = line.split("\t")[1]
            if pattern.match(standing):
                name = nameDict.get(number)
                decklistDict[name] = (standing)
                seenName = False
                seenNumber = False

def parsePage(decklistDict, lines):
    seenPoints = False
    seenNumber = False
    seenName = False
    seenDecklist = False
    number = 0

    pointsPattern = re.compile("Points")
    numberPattern = re.compile("[0-9]+")
    pattern = re.compile("([0-9]+(-[0-9]+)+)")
    endPattern = re.compile("Displaying")
    decklistPattern = re.compile("[A-Za-z]+")
    decklistPattern2 = re.compile("^(?!.*>).*")

    for line in lines:

        if endPattern.match(line):
            return

        if pointsPattern.match(line):
            seenPoints = True

        if not seenPoints:
            continue

        if numberPattern.match(line):
            seenNumber = True
            number = int(line)
        elif seenNumber and not seenName:
            name = line.split('<')[0]
            decklistDict[number] = (name, "", "")
            seenName = True
        elif seenNumber and seenName and not seenDecklist:
            if len(line.split('<')) > 0:
                if decklistPattern.match(line.split('<')[0]) and decklistPattern2.match(line.split('<')[0]):
                    decklistName = line.split('<')[0]
                    entry = decklistDict.get(number)
                    decklistDict[number] = (entry[0], decklistName, "")
                    seenDecklist = True
        elif seenNumber and seenNumber and seenDecklist:
            if len(line.split("\t")) <= 1:
                    continue

            standing = line.split("\t")[1]
            if pattern.match(standing):
                entry = decklistDict.get(number)
                decklistDict[number] = (entry[0], entry[1], standing)
                seenName = False
                seenNumber = False
                seenDecklist = False
    
def readDraft():
    # draft
    nameDict = {}
    draftDict = {}
    path = 'decklistRaws/draft'
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            f = open(os.path.join(path, file), 'r', encoding="utf8")
            lines = f.readlines()
            parseDraft(draftDict, lines, nameDict)
            f.close()
    return draftDict

def readConstructed():
    # constructed
    decklistDict = {}
    path = 'decklistRaws/constructed'
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            f = open(os.path.join(path, file), 'r', encoding="utf8")
            lines = f.readlines()
            parsePage(decklistDict, lines)
            f.close()
    return decklistDict

def writeConstructed(decklistDict):
    with open('constructed_deck_standings.csv', 'w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws"))
        for key, value in decklistDict.items():
            record = value[2].split('-')
            if(len(record)<3):
                continue
            writer.writerow([key, value[0], value[1], record[0], record[1], record[2]])

def writeDraft(decklistDict):
    with open('draft_standings.csv', 'w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Name', "Wins", "Losses", "Draws"))
        for key, value in decklistDict.items():
            record = value.split('-')
            if(len(record)<3):
                continue
            writer.writerow([key, record[0], record[1], record[2]])

def writeCombined(decklistDict, draftDict):
    with open('combined_standings.csv', 'w', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws", "Draft Record"))
        for key, value in decklistDict.items():
            record = value[2].split('-')
            if(len(record)<3):
                continue
            draftRecord = draftDict.get(value[0])
            writer.writerow([key, value[0], value[1], record[0], record[1], record[2], draftRecord])

decklistDict = {}

response = int(input("0 = constructed\n 1 = limited\n 2 = combined\n"))

if response == 0 :
    decks = readConstructed()
    writeConstructed(decks)
elif response == 1 :
    decks = readDraft()
    writeDraft(decks)
elif response == 2:
    constructed = readConstructed()
    draft = readDraft()
    writeCombined(constructed, draft)

else:
    print("Input was invalid")
