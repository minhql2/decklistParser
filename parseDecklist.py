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


with open('decklists.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws"))
    for key, value in decklistDict.items():
        record = value[2].split('-')
        if(len(record)<3):
            continue
        writer.writerow([key, value[0], value[1], record[0], record[1], record[2]])
    