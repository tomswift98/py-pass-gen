__author__ = 'Liam Bennett'

import tkinter as tk
import random
import re
import webbrowser
from math import log, pow
import sys


class MainWindow(tk.Frame):

    def __init__(self, master=None):

        tk.Frame.__init__(self, master)
        self.init_window()

    def init_window(self):
        self.master.title("py-pass-gen")
        self.pack(fill=tk.BOTH, expand=1)

        self.frame = tk.LabelFrame(self, relief=tk.GROOVE, borderwidth=1,
                                   text="Passphrase Settings",
                                   labelanchor=tk.NE)
        self.frame.pack(fill=tk.BOTH, expand=1, side=tk.TOP)

        # code for scale widgets to input passphrase settings
        words = tk.IntVar()
        s = tk.Scale(self.frame, from_=1, to=12, orient=tk.HORIZONTAL,
                     length=200, label='Number of terms:', variable=words)
        s.pack(expand=True, side=tk.TOP)
        s.set(5)

        caps = tk.IntVar()
        s = tk.Scale(self.frame, from_=0, to=12, orient=tk.HORIZONTAL,
                     length=200, label='Number of capital letters:',
                     variable=caps)
        s.pack(expand=True, side=tk.TOP)
        s.set(2)

        nums = tk.IntVar()
        s = tk.Scale(self.frame, from_=0, to=12, orient=tk.HORIZONTAL,
                     length=200, label='Number of digits:', variable=nums)
        s.pack(expand=True, side=tk.TOP)
        s.set(1)

        chars = tk.IntVar()
        s = tk.Scale(self.frame, from_=0, to=12, orient=tk.HORIZONTAL,
                     length=200, label='Number of special characters:',
                     variable=chars)
        s.pack(expand=True, side=tk.TOP, pady=5)
        s.set(1)

        # menu settings
        ow = tk.IntVar()
        self.display_steps = tk.IntVar()
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file = tk.Menu(menu, tearoff=0)
        file.add_command(label="Entropy Calculator",
                         command=self.entropy_calculator_click)
        file.add_checkbutton(label='Display steps',
                             variable=self.display_steps,
                             onvalue=1, offvalue=0)
        file.add_checkbutton(label='Overwrite letters', variable=ow, onvalue=1,
                             offvalue=0)
        file.add_command(label="About", command=self.about_application)
        file.add_command(label="Quit", command=self.quit)
        # self.master.bind('<Escape>', lambda f, q=file: self.quit)

        menu.add_cascade(label="Menu", menu=file)

        b = tk.Button(self, text="Generate Passphrase",
                      command=lambda w=words, c=caps, n=nums, ch=chars,
                      ow=ow: self.password_button_click(words.get(),
                                                        caps.get(),
                                                        nums.get(),
                                                        chars.get(),
                                                        ow.get()),
                      padx=10, pady=5)
        self.master.bind('<Return>', (lambda e, b=b: b.invoke()))
        b.pack(side=tk.BOTTOM, padx=10, pady=5)

    def entropy_calculator_click(self):
        EntropyCalcWindow(root)

    def password_button_click(self, wrds, caps, nums, chars, ow):
        FILE = 'dict.txt'

        password = PassWord()
        password.create_password(FILE, wrds, caps, nums, chars, ow)

        word = password.get_password()

        top = tk.Toplevel()

        top.wm_iconbitmap(bitmap="icon.ico")
        top.grab_set()
        top.focus()
        top.title('Result')
        top.minsize(width=10, height=10)

        txt = tk.Label(top, text=word, font=('Ariel', 16), padx=10)
        txt.pack(expand=True, side=tk.TOP)

        entropy = password.get_entropy()
        entropy = "Entropy: " + str(entropy) + " bits"

        ent = tk.Label(top, text=entropy, font=('Ariel', 10), padx=10)
        ent.pack(expand=True, side=tk.TOP)

        combs = password.get_combs()
        combinations = "Possible Passwords > " + "{:.1e}".format(combs)

        comb = tk.Label(top, text=combinations, font=('Ariel, 10'), padx=10)
        comb.pack(expand=True, side=tk.TOP)

        if self.display_steps.get() == 1:
            steppy_words = 'Step by Step Breakdown: \n1. ' \
                + password.get_words() + '\n2. ' + password.get_caps() \
                + '\n3. ' + password.get_nums() + '\n4. ' \
                + password.get_specials()
            txtsteps = tk.Label(top, text=steppy_words,
                                font=('Ariel', 10), padx=10)
            txtsteps.pack(expand=True, side=tk.TOP)

        button = tk.Button(top, text="Back",
                           command=top.destroy, padx=75, pady=5)
        button.pack(side=tk.TOP, pady=5, padx=10)
        top.bind('<Return>', (lambda e, b=button: b.invoke()))  # binds enter

    def about_application(self):
        webbrowser.open("README.md")


class EntropyCalcWindow(tk.Frame):

    def __init__(self, master=None):
        self.init_window()

    def init_window(self):

        top = tk.Toplevel(root)
        top.title("Entropy Calculator")
        top.wm_iconbitmap(bitmap="icon.ico")
        top.grab_set()
        top.minsize(width=250, height=75)

        self.t = tk.Label(top,
                          text="Enter a passphrase to calculate its entropy:")
        self.t.pack(side=tk.TOP)

        self.e = tk.Entry(top, width='42')
        self.e.pack(padx=5, side=tk.TOP)
        self.e.focus()

        self.b = tk.Button(top, text="Calculate Entropy", command=self.execute,
                           pady=5, padx=10)
        self.b.pack(side=tk.RIGHT, pady=5, padx=10)
        top.bind('<Return>', (lambda e, b=self.b: b.invoke()))  # b is button

        self.b = tk.Button(top, text="Back", command=top.destroy,
                           pady=5, padx=10)
        top.bind('<Escape>', (lambda e, b=self.b: b.invoke()))  # binds enterkey
        self.b.pack(side=tk.LEFT, pady=5, padx=10)

    def execute(self):

        top = tk.Toplevel()  # creation of result window

        # result window settings
        top.wm_iconbitmap(bitmap="icon.ico")
        top.grab_set()
        top.focus()
        top.minsize(width=210, height=10)
        top.title('Entropy')

        password = self.e.get()

        self.txt = tk.Label(top, text=password, font=('Ariel', 16), padx=10)
        self.txt.pack()

        self.entropy = calculate_entropy(password=password)
        self.entropystr = "Entropy: " + self.entropy + " bits"

        self.ent = tk.Label(top, text=(self.entropystr), font=('Ariel', 8),
                            padx=10)
        self.ent.pack(expand=True, side=tk.TOP)

        self.b = tk.Button(top, text="Back", command=top.destroy,
                           padx=10, pady=5)
        self.b.pack(pady=5, padx=10)
        top.bind('<Return>', (lambda e, b=self.b: self.b.invoke()))
        top.bind('<Escape>', (lambda e, b=self.b: self.b.invoke()))


def calculate_entropy(password=''):

    numeric = re.compile('\d')
    loweralpha = re.compile('[a-z]')
    upperalpha = re.compile('[A-Z]')
    symbols = re.compile(r'~#%+-*^=@/\\|<\'>()`&_!?.,:;')  # same as pass gen
    num_of_symbols = 26  # number of symbols in set

    charset = 0
    if numeric.search(password):
        charset += 10
    if loweralpha.search(password):
        charset += 26
    if upperalpha.search(password):
        charset += 26
    if symbols.search(password):
        charset += num_of_symbols

    try:
        entropy = log(pow(charset, len(password)), 2)
        entropy = str(round(entropy, 2))

    except ValueError:
        entropy = "Error!"

    return entropy


class PassWord():

    def __init__(self):
        self.password = ''

    def create_password(self, FILE, wrds, caps, nums, chars, ow):
        char_list = '~#%+-*^=@/\\|<\'>()`&_!?.,:;'  # same as entropy calc
        num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        word = ''
        words = []
        self.verbs = 'No action taken.'
        self.digits = 'No action taken.'
        self.caps = 'No action taken.'
        self.figures = 'No action taken.'
        self.word_list_length = 0
        self.entropy = 0

        while True:
            try:
                f = open(FILE, 'r')
                lines = f.readlines()   # reads all dictonary lines to list
                f.close()
                break

            except FileNotFoundError:
                print('Error: Dictionary file not found.')
                sys.exit(1)

        for line in lines:      # reads each line in file
            word = line.strip()
            words.append(word)

        x = 0
        indexes = []

        self.word_list_length = len(lines)

        # ow overwrite variable become important here; offsets character insert
        while x < wrds:    # adds words to list
            n = random.SystemRandom().randint(1, self.word_list_length)
            indexes.append(n)
            x += 1

        for index in indexes:  # appends next word to password string
            self.password = self.password + words[index]
            self.verbs = self.password

        x = 0
        while x < caps:  # randomly adds uppercase chars until quota is met
            index = random.SystemRandom().randint(0, (len(self.password) - 1))
            letter = self.password[index].upper()
            self.password = self.password[:index] + letter \
                + self.password[(index + 1):]
            self.caps = self.password
            x += 1

        x = 0
        while x < nums:     # randomly adds digits until quota is met
            some_num = random.choice(num_list)
            index = random.SystemRandom().randint(0, (len(self.password) - 1))
            self.password = self.password[:index] \
                + some_num + self.password[(index + ow):]
            self.digits = self.password
            x += 1

        x = 0
        while x < chars:  # randomly adds special characters until quota is met
            some_char = random.choice(char_list)
            index = random.SystemRandom().randint(0, (len(self.password) - 1))
            self.password = self.password[:index] \
                + some_char \
                + self.password[(index + ow):]
            self.figures = self.password
            x += 1

        n = len(self.password)

        # this is not correct, will do better combinatorics later
        self.possible_passwords = self.word_list_length ** wrds \
            * 26 ** caps * n \
            * 10 ** nums * n \
            * 26 ** chars * n

        self.entropy = calculate_entropy(self.password)

    def get_entropy(self):
        return self.entropy

    def get_words(self):
        return self.verbs

    def get_nums(self):
        return self.digits

    def get_specials(self):
        return self.figures

    def get_caps(self):
        return self.caps

    def get_combs(self):
        return self.possible_passwords

    def get_password(self):
        return self.password


# creation of root window
root = tk.Tk()
root.resizable(width=tk.FALSE, height=tk.FALSE)
root.geometry("250x330")
root.wm_iconbitmap(bitmap="icon.ico")

# creation of a program instance
app = MainWindow(root)
# mainloop
root.mainloop()
