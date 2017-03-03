import random

#Given a string formatted like "2d20", rolls the requested number of dice
def rollDice(diceString):
    rollInformation = parseString(diceString)
    rollResults = []
    if rollInformation:
        for i in range(rollInformation[0]):
            rollResults.append(random.randint(1, rollInformation[1]))
        return rollResults
    else:
        return None

#Currently assumes a structure of "xdy"
def parseString(diceString):
    splitString = diceString.split('d')
    rollInformation = []
    rollInformation.append(int(splitString[0]))
    rollInformation.append(int(splitString[1]))
    return rollInformation
