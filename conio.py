'''Module providing high-level input/output functionality'''

import os

def msg(msg):
    '''Prints a single- or multi lined message to the screen.'''
    print(msg)

def textIn(prompt):
    '''Prompt the user to input a text input.'''
    s = input(prompt)
    return s

def numIn(prompt):
    '''Prompt the user to input a numeral input.'''
    while(True):
        try:
            n = float(input(prompt))
        except ValueError:
            print("Please enter a number!")
        else:
            return n

def binChoice(prompt):
    '''Prompt the user to input a binary choice (y/n).'''
    while True:
        choice = input("{} (y/n) ".format(prompt))
        if choice == ('y'):
            return True
        elif choice == ('n'):
            return False
        msg("Invalid answer.")

def menu(prompt, choices, abort=None):
    '''Prompt the user to input a numeral menu choice.

    Parameters:
    prompt -- prompt string
    choices -- list of strings
    abort -- string indicating an additional abort choice

    Returns:
    index of selected choice, -1 if aborted
    '''
    skipLine()
    msg(prompt)
    skipLine()
    for i, choice in enumerate(choices):
        print("  {} - {}".format(str(i+1), choice))
    if abort is not None:
        skipLine()
        print("  {} - {}".format(str(len(choices)+2), abort))
    skipLine()
    while True:
        choice = int(numIn("> ")-1)
        if choice >= 0 and choice < len(choices):
            return choice
        elif choice == len(choices)+1:
            return -1
        msg("Please enter a valid choice")

def skipLine(amount=1):
    '''Skips amount amount of lines'''
    if amount > 0:
        out = ""
        for line in range(amount-1):
            out += "\n"
        print(out)

def table(data, spacing=5):
    '''Constructs and displays a table from data given

    Parameters
    data -- 2D list containing data (data[row][col])
    spacing -- additional column spacing
    '''
    rows = len(data)
    cols = 0

    # Get amount of rows
    for row in range(rows):
        cols = len(data[row])
    colWidths = [0]*cols

    # Get minimum width for each column
    for row in range(rows):
        for col in range(cols):
            if len(str(data[row][col])) > colWidths[col]:
                colWidths[col] = len(str(data[row][col]))

    # Format and print rows
    for row in range(rows):
        rowstr = ""
        for col in range(cols):
            if col == cols-1:
                rowstr += "{}"
            else:
                rowstr += "{:<"+str(colWidths[col]+spacing)+"}"
        print(rowstr.format(*data[row]))

def progressBar(value, valueMax, length, label="", displayValues=False):
    '''Constructs and displays a progress bar based on given value and max value.

    Parameters:
    value -- current value
    valueMax -- maximum value
    length -- bar length
    label -- bar label
    displayValues -- displays values and percentage on bar if True
    '''
    bar = ""
    bar += int(length*(value/valueMax))*"="
    bar += int(length-length*(value/valueMax))*"-"
    if displayValues:
        displayText = "{}/{}{}({}%)".format(value, valueMax, bar[int(length/2)], 100*round(value/valueMax, 4))
        charList = list(bar)
        if length < len(displayText):
            length = len(displayText)
        for i in range(len(displayText)):
            charList[int(len(bar)/2-len(displayText)/2+i)]=displayText[i]
        bar = "".join(charList)
    header = " "
    header += " "*int(len(bar)/2-len(label)/2)
    header += label
    print(header)
    print("["+bar+"]")

def cls():
    '''Clears the screen'''
    os.system('cls' if os.name == 'nt' else 'clear')
