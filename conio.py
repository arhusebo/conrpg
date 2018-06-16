'''Module providing high-level input/output functionality'''

import os
from textwrap import dedent

def msg(msg):
    """Prints a single- or multi lined message to the screen."""
    print(dedent(msg.strip('\n')))

def text_in(prompt):
    """Prompt the user to input a text input."""
    s = input(prompt)
    return s

def num_in(prompt):
    """Prompt the user to input a numeral input."""
    while(True):
        try:
            n = float(input(prompt))
        except ValueError:
            print("Please enter a number!")
        else:
            return n

def bin_choice(prompt):
    """Prompt the user to input a binary choice (y/n)."""
    while True:
        choice = input("{} (y/n) ".format(prompt))
        if choice == ('y'):
            return True
        elif choice == ('n'):
            return False
        msg("Invalid answer.")

def menu(prompt, choices, abort=None):
    """Prompt the user to input a numeral menu choice.

    Parameters:
    prompt -- prompt string
    choices -- list of strings
    abort -- string indicating an additional abort choice

    Returns:
    index of selected choice, -1 if aborted
    """
    skip_line()
    msg(prompt)
    skip_line()
    for i, choice in enumerate(choices):
        print("  {} - {}".format(str(i+1), choice))
    if abort is not None:
        skip_line()
        print("  {} - {}".format(str(len(choices)+2), abort))
    skip_line()
    while True:
        choice = int(num_in("> ")-1)
        if choice >= 0 and choice < len(choices):
            return choice
        elif choice == len(choices)+1:
            return -1
        msg("Please enter a valid choice")

def skip_line(amount=1):
    """Skips amount amount of lines"""
    if amount > 0:
        out = ""
        for line in range(amount-1):
            out += '\n'
        print(out)

def table(data, spacing=5):
    """Constructs and displays a table from data given

    Parameters
    data -- 2D list containing data (data[row][col])
    spacing -- additional column spacing
    """
    rows = len(data)
    cols = 0

    # Get amount of rows
    for row in range(rows):
        cols = len(data[row])
    col_widths = [0]*cols

    # Get minimum width for each column
    for row in range(rows):
        for col in range(cols):
            if len(str(data[row][col])) > col_widths[col]:
                col_widths[col] = len(str(data[row][col]))

    # Format and print rows
    for row in range(rows):
        rowstr = ""
        for col in range(cols):
            if col == cols-1:
                rowstr += "{}"
            else:
                rowstr += "{:<"+str(col_widths[col]+spacing)+"}"
        print(rowstr.format(*data[row]))

def progress_bar(value, value_max, length, label="", display_values=False):
    """Constructs and displays a progress bar based on given value and max value.

    Parameters:
    value -- current value
    value_max -- maximum value
    length -- bar length
    label -- bar label
    display_values -- displays values and percentage on bar if True
    """
    bar = ""
    bar += int(length*(value/value_max))*"="
    bar += int(length-length*(value/value_max))*"-"
    if display_values:
        display_text = "{}/{}{}({}%)".format(value, value_max, bar[int(length/2)], 100*round(value/value_max, 4))
        char_list = list(bar)
        if length < len(display_text):
            length = len(display_text)
        for i in range(len(display_text)):
            char_list[int(len(bar)/2-len(display_text)/2+i)]=display_text[i]
        bar = "".join(charList)
    header = " "
    header += " "*int(len(bar)/2-len(label)/2)
    header += label
    print(header)
    print("["+bar+"]")

def cls():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
