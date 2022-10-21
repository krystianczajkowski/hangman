# hangman
import os
from random import choice
from time import sleep

HANGMAN = ["""
     ____
    |/   |
    |   
    |    
    |    
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |    
    |    
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |    |
    |    |    
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \|
    |    |
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \|/
    |    |
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \|/
    |    |
    |   / 
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \|/
    |    |
    |   / \\
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   /|\\
    |    |
    |   | |
    |
    |_____
    """
           ]
SUPPORTED_LANGUAGES = ['polish', 'english']
# default language is english
DEFAULT_LANGUAGE = SUPPORTED_LANGUAGES[1]

def main():
    try:
        play_game(get_word(input('Wybierz poziom trudności: 1 - łatwy, 2 - trudny ')))
    except ValueError:
        main()

# make function to get word from file
def get_word(level: int) -> str:
    if int(level) == 2:
        with open('slowa.txt', encoding='utf-8') as f:
            return choice(f.readlines()).strip()
    else:
        with open('wyrazy.txt', encoding='utf-8') as f:
            return choice(f.readlines()).strip().lower()
    

def find_lttr(word, g_word, lttr):
    if lttr.lower() == word:
        return word
    for i, l in enumerate(word):
        if l == lttr:
            g_word[i] = word[i]
    return g_word

# function to guess


def play_game(word):
    wrong_lttrs = ''
    g_word = ['_' for i in word]
    tries = 0
    os.system('cls')
    print(' ')
    print('Długość słowa:', len(word))

    while tries != len(HANGMAN):
        print(' '.join(g_word).upper())
        if tries == 0:
            guess = input('Wprowadź literę: ')
        else:
            guess  = input('Wprowadź literę lub zgadnij słowo: ')
        if guess.lower() not in word:
            print(HANGMAN[tries])
            tries += 1
            wrong_lttrs += guess.upper()[0]
            if wrong_lttrs:
                print('Wprowadzone litery: ', ' '.join(wrong_lttrs))
        else:
            g_word = find_lttr(word, g_word, guess)
            if ''.join(g_word) == word:
                print(word.upper())
                print('WYGRAŁEŚ')
                sleep(10)
                break

    if tries == len(HANGMAN):
        print('RIP')
        print('Słowo klucz:', word.upper())
        sleep(10)

if __name__ == "__main__":
    main()
