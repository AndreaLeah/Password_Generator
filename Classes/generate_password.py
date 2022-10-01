from random import *

# CONSTANTS
LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z']
UPPER_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '@', '#', '$', '%', '&', '*']


# '(', ')', '+'
class GeneratePassword:
    # Automatically generates password each time, generates new password when
    # 'generate password' button pressed & copies the password to clipboard
    def __init__(self):

        # Generate 5-8 lowercase letters
        self.lower_chars = [choice(LETTERS) for char in range(5)]
        # Generate 5-8 uppercase letters
        self.upper_chars = [choice(UPPER_LETTERS) for u_char in range(6)]
        # Generate 4-8 integers
        self.nums = [choice(NUMBERS) for num in range(4)]
        # Generate 4-8 symbols
        self.symbs = [choice(SYMBOLS) for sym in range(5)]

        # Generate & return password
        self.gen_password()

    def gen_password(self) -> str:
        # Add all generated characters
        self.password_list = self.lower_chars + self.upper_chars + self.nums + self.symbs
        shuffle(self.password_list)

        # Join all items together into a string
        # https://www.w3schools.com/python/ref_string_join.asp
        self.password = ''.join(self.password_list)
        return self.password

