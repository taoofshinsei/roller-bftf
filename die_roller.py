import random

#Given a string formatted like "2d20[+-]a...[+-]z", rolls the requested number of dice
#and sums the modifiers
def rollDice(diceString):
    rollInformation = parseString(diceString)
    rollResults = []
    if rollInformation:
        for i in range(rollInformation[0]):
            rollResults.append(random.randint(1, rollInformation[1]))
        rollResults.append(rollInformation[2])
        return rollResults
    else:
        return None

#Currently assumes a structure of "mdn[+-]o[+-]p..[+-]z"
#Returns a three element list. L[0] is # of dice, L[1] is size, L[2] is total mod
def parseString(diceString):
    splitString = diceString.split('d')
    rollInformation = []
    rollInformation.append(int(splitString[0]))
    rollInformation.extend(sumModifiers(splitString[1]))
    return rollInformation

#Given a string of "a[+-]b[+-]c...[+-]z", sumModifiers extracts a and sums b-z
#Returns a list of two elements. Element 0 is a (the size of the die), elem 1 is the sum
def sumModifiers(dieSizeWithMods):
    splitOnPlus = testString.split('+', 1)
    splitOnMinus = testString.split('-', 1)
    if len(splitOnPlus) == 1 and len(splitOnMinus) == 1:
        #No modifiers to speak of, just add a 0 to insure a two element array
        splitOnPlus[0] = int(splitOnPlus[0])
        splitOnPlus.append(0)
        return splitOnPlus
    elif len(splitOnPlus[0]) < len(splitOnMinus[0]):
        #Plus came before minus, so the first modifier better be positive
        splitOnPlus[0] = int(splitOnPlus[0])
        splitOnPlus[1] = eval(splitOnPlus[1])
        return splitOnPlus
    else:
        #Minus came before plus, so the first modifier better be negative
        splitOnMinus[0] = int(splitOnMinus[0])
        #Reinsert that negative at the beginning
        splitOnMinus[1] = eval('-' + splitOnMinus[1])
        return splitOnMinus
