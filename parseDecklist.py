import csv
import re
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

decklistDict = {}

file2 = open('rawFileConstructed.txt', 'r')
lines2 = file2.readlines()

parsePage(decklistDict, lines2)


with open('decklists.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws"))
    for key, value in decklistDict.items():
        record = value[2].split('-')
        if(len(record)<3):
            continue
        writer.writerow([key, value[0], value[1], record[0], record[1], record[2]])
    