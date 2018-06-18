'''Module providing high-level input/output functionality'''

import os
from textwrap import dedent

class Graphics:
    """Instantiable class for loading and displaying UTF-8 encoded graphics"""
    def __init__(self, path):
        self.path = path

    def load(self):
        self.data = {}
        with open(self.path, 'r', encoding='utf-8') as f:
            self.data_raw = f.read()
            for d in self.data_raw.split('<')[1:]:
                data = d.split('>')
                self.data.update({data[0]: data[1]})

    def draw(self, name):
        print(self.data[name])

    def list_graphics(self):
        out = ""
        nl = '\n'
        for key in self.data.keys():
            out += dedent(f"""{key}
            height: {self.data[key].count(''.join(nl))}
            width:  {len(max(self.data[key].split(nl)))}
            """)
        print(out)

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
    
    choice_map = {}
    for i, choice in enumerate(choices):
        choice_map[i+1] = choice
        print(f"  {i+1} - {choice}")
    if abort:
        choice_map[len(choices)+1] = abort
        skip_line()
        print(f"  {len(choices)+1} - {abort}")
    skip_line()
    while True:
        choice_key = int(num_in("> "))
        if choice_map.get(choice_key):
            return choice_map[choice_key]
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
    bar = int(length*(value/value_max))*"="
    bar = bar.ljust(length, "-")
    if display_values:
        display_text = f"{value}/{value_max}{bar[int(length/2)]}({100*value/value_max:.1f}%)"
        char_list = list(bar)
        if length < len(display_text):
            length = len(display_text)
        #FIX next part is unreadable
        for i in range(len(display_text)):
            char_list[int(len(bar)/2-len(display_text)/2+i)]=display_text[i]
        bar = "".join(char_list)
    header = " "
    header += " "*int(len(bar)/2-len(label)/2)
    header += label
    print(header)
    print(f"[{bar}]")

def cls():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
