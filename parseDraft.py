import csv
import re

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

file1 = open('rawFileBetter.txt', 'r')
lines1 = file1.readlines()

decklistDict = {}
nameDict = {}

parseDraft(decklistDict, lines1, nameDict)

with open('decklists.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws"))
    for key, value in decklistDict.items():
        record = value.split('-')
        if(len(record)<3):
            continue
        writer.writerow([key, record[0], record[1], record[2]])
    