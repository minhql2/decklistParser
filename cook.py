import csv

def parsePage(decklistDict, count, dictCount, lines):
    for line in lines:
        count+=1
        if (((count+2) % 5) == 0 and count > 2):
            name = line.split('<')[0]
            decklistDict[dictCount] = (name, "", "")
        elif (count % 5 == 0):
            decklist = line.split('<')[0]
            decklist1 = decklistDict.get(dictCount)
            decklistDict[dictCount] = (decklist1[0], decklist, "")
        elif ((((count-1) % 5) == 0) and count > 5):
            if(len(line.split("\t")) <= 1):
                continue
            standing = line.split("\t")[1]
            decklist = decklistDict.get(dictCount)
            decklistDict[dictCount] = (decklist[0], decklist[1], standing)
            dictCount+=1

def parseDraft(decklistDict, count, dictCount, lines, nameDict):
    for line in lines:
        count+=1
        if (((count+3) % 5) == 0 and count > 1):
            name = line.split('<')[0]
            nameDict[dictCount] = name
        elif (count % 5 == 0):
            if(len(line.split("\t")) <= 1):
                continue
            standing = line.split("\t")[1]
            name = nameDict.get(dictCount)
            decklistDict[name] = (standing)
            dictCount+=1

# parse day 2 decklists
file1 = open('page1Text.txt', 'r')
lines1 = file1.readlines()

decklistDict = {}

count = 0
dictCount = 0
parsePage(decklistDict, count, dictCount, lines1)

file2 = open('page2Text.txt', 'r')
lines2 = file2.readlines()

count = 100
dictCount = 100
parsePage(decklistDict, count, dictCount, lines2)

# parse draft decklists
file1 = open('draft1.txt', 'r')
lines1 = file1.readlines()

draftDecklistDict = {}
nameDict = {}

count = 0
dictCount = 0
parseDraft(draftDecklistDict, count, dictCount, lines1, nameDict)

file2 = open('draft2.txt', 'r', encoding="utf8")
lines2 = file2.readlines()

count = 100
dictCount = 100
parseDraft(draftDecklistDict, count, dictCount, lines2, nameDict)

file3 = open('draft3.txt', 'r')
lines3 = file3.readlines()

count = 200
dictCount = 200
parseDraft(draftDecklistDict, count, dictCount, lines3, nameDict)


with open('complete data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws", "Draft Record"))
    for key, value in decklistDict.items():
        record = value[2].split('-')
        if(len(record)<3):
            continue
        draftRecord = draftDecklistDict.get(value[0])
        writer.writerow([key, value[0], value[1], record[0], record[1], record[2], draftRecord])
    