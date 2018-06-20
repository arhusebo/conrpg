"""Module providing high-level input/output functionality"""

import os
import math as m
from textwrap import dedent
import listener

underline = lambda c: '\033[4m'+c+'\033[0m'

class Graphics:
    """Instantiable class for loading and displaying UTF-8 encoded graphics"""

    charsets = {'unicode':u' \u2591\u2592\u2593\u2588',
                'ascii':' '+chr(9617)+chr(9618)+chr(9619)+chr(9608),
                'ascii2':' .:-=+*#%@'}

    def __init__(self, path, charset):
        self.path = path
        if charset in Graphics.charsets:
            self.charset = Graphics.charsets[charset]
        else:
            self.charset = self.charsets['ascii']

    def load(self):
        self.data = {}
        with open(self.path, 'r') as f:
            self.data_raw = f.read()
            for d in self.data_raw.split('<')[1:]:
                data = d.split('>')
                self.data.update({data[0]: data[1]})

    def draw(self, name):
        out = ""
        lines = self.data[name].split('\n')
        for line in lines:
            for i in line:
                out += self.charset[int((len(self.charset)-1)*int(i)/9)]
            out += '\n'
        print(out)

    def list_graphics(self):
        out = ""
        nl = '\n'
        for key in self.data.keys():
            out += dedent(f"""{key}
            height: {self.data[key].count(''.join(nl))}
            width:  {len(max(self.data[key].split(nl)))}
            """)
        print(out)

def msg(msg, end='\n'):
    """Prints a single- or multi lined message to the screen."""
    print(dedent(msg.strip('\n')), end=end)

def acknowledge(msg='', end='\n'):
    """Prints a single- or multi lined message to the screen."""
    print(dedent(msg.strip('\n')), end=end)
    print("\nPress any key to return.")
    listener.get_key()
    
def text_in(prompt):
    """Prompt the user to input a text input."""
    return input(prompt)

def num_in(prompt):
    """Prompt the user to input a numeral input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number!")

def bin_choice(prompt, default='y'):
    """Prompt the user to input a binary choice (y/n)."""
    choices = {
        'y' : "(Y/n)",
        'n' : "(y/N)",
    }.get(default, "(y/n)")

    choice = None
    while 1:
        choice = input(f"{prompt} {choices}: ").lower()
        if default and choice == '':
            choice = default
        if choice in {'y', 'n'}:
            return choice == 'y'
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
        choice_map[str(i+1)] = choice
        print(f"  {i+1} - {choice}")
    if abort:
        skip_line()
        choice_map[str(len(choices)+1)] = choice_map['ESC'] = abort
        print(f"  {len(choices)+1} - {abort} ({underline('Esc')})")
    skip_line()
    while True:
        choice_key = listener.get_key("> ")
        if choice_key in choice_map:
            return choice_map[choice_key]
        msg("Please enter a valid choice")

def map_menu(prompt, choices, abort=None):
    """Prompt the user to input a numeral menu choice.

    Parameters:
    prompt  -- prompt string
    choices -- list of strings
    abort   -- string indicating an additional abort choice

    Returns:
    selected choice
    """
    msg(prompt)
    choice_map = {}
    for key in choices:
        if key == abort: continue
        i = key.index('*')
        k = key[i+1]
        choice_map[k.lower()] = choice_map[k.upper()] = key
        print(f"  - "+key[:i]+underline(k)+key[i+2:])
    if abort:
        i = abort.index('*')
        k = abort[i+1]
        choice_map[k.lower()] = choice_map[k.upper()] = choice_map['ESC'] = key
        print(f"  - "+abort[:i]+underline(k)+abort[i+2:]+f" ({underline('Esc')})")
    
    skip_line()
    while True:
        choice_key = listener.get_key("> ")
        print(repr(choice_key))
        if choice_key in choice_map:
            return choice_map[choice_key]
        msg("Please enter a valid choice")

def skip_line(amount=1):
    print('\n'*amount, end='')

def table(*data, spacing=5):
    """Constructs and displays a table from data given

    Parameters
    data    -- 2D list containing data (data[row][col])
    spacing -- additional column spacing
    """
    
    # Get minimum width for each column
    col_widths = [len(max(col, key=lambda x: len(str(x)))) for col in zip(*data)]

    # Format and print rows
    for row in data:
        for col, w in zip(row, col_widths):
            print(str(col).ljust(w+spacing), end='')
        print() #newline

def progress_bar(value, value_max, length, label="", display_values=False):
    """Constructs and displays a progress bar based on given value and max value.

    Parameters:
    value          -- current value
    value_max      -- maximum value
    length         -- bar length
    label          -- bar label
    display_values -- displays values and percentage on bar if True
    """
    progress_ratio = value/value_max
    bar = ("="*m.floor(length*progress_ratio)).ljust(length, "-")

    if display_values:
        progress = f"{value}/{value_max}"
        progress_percent = f"({100*progress_ratio:.1f}%)"
        mid = m.floor(length/2)
        try:
            # Inserts progress inside bar
            bar = (bar[:mid-len(progress)]
                + progress
                + bar[mid:mid+1]
                + progress_percent
                + bar[mid+1+len(progress_percent):]
            )
        except Exception:
            # Fails if bar is too short
            pass

    header = label.rjust(mid+m.ceil(len(label)/2)+1)
    print(header)
    print(f"[{bar}]")

def cls():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
