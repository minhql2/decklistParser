import csv

def parsePage(decklistDict, count, dictCount, lines):
    for line in lines:
        count+=1
        if (((count+3) % 5) == 0 and count > 1):
            name = line.split('<')[0]
            decklistDict[dictCount] = (name, "")
        elif (count % 5 == 0):
            if(len(line.split("\t")) <= 1):
                continue
            standing = line.split("\t")[1]
            decklist = decklistDict.get(dictCount)
            decklistDict[dictCount] = (decklist[0], standing)
            dictCount+=1

file1 = open('draft1.txt', 'r')
lines1 = file1.readlines()

decklistDict = {}

count = 0
dictCount = 0
parsePage(decklistDict, count, dictCount, lines1)

file2 = open('draft2.txt', 'r', encoding="utf8")
lines2 = file2.readlines()

count = 100
dictCount = 100
parsePage(decklistDict, count, dictCount, lines2)

file3 = open('draft3.txt', 'r')
lines3 = file3.readlines()

count = 200
dictCount = 200
parsePage(decklistDict, count, dictCount, lines3)


with open('decklists.csv', 'w', encoding="utf8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('Standing', 'Deck', "Wins", "Losses", "Draws"))
    for key, value in decklistDict.items():
        record = value[1].split('-')
        if(len(record)<3):
            continue
        writer.writerow([key, value[0], record[0], record[1], record[2]])
    