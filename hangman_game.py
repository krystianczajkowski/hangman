# hangman

from random import choice
from time import sleep
from blessed import Terminal

term = Terminal()
HANGMAN = ("""
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
    |   \\|
    |    |
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \\|/
    |    |
    |    
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \\|/
    |    |
    |   / 
    |
    |_____
    """,
           """
     ____
    |/   |
    |   (_)
    |   \\|/
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
)
SUPPORTED_LANGUAGES = ['polish', 'english']
# default language is english
def main():
    
    play_game(get_word(select_language(input(f'Choose your language: {SUPPORTED_LANGUAGES} '))))

def select_language(lang: str) -> str:
    if lang.lower() in SUPPORTED_LANGUAGES:
        return lang.lower()
    else: 
        print(f'{term.red2}Language: {term.cornflowerblue}{lang}{term.red2} unsupported! Defaulting to English.{term.normal}')
        sleep(1)
        return 'english'

def get_word(language: str) -> str:
    """Grabs a random word from a .txt file"""
    with open(f'{language}.txt', encoding='utf-8') as f:
        return choice(f.readlines()).strip().lower()
        

def find_lttr(word: str, g_word: list, lttr: str) -> str:
    """Searches one string for a letter and if it finds it replaces it in second string."""
    if lttr.lower() == word:
        g_word = word
        return g_word
    elif len(lttr) > 1:
        lttr = lttr[0]
    for i, l in enumerate(word):
        if l == lttr:
            g_word[i] = word[i]
    return g_word



def play_game(word):
    """Main function of the program"""
    
    wrong_lttrs = ''
    g_word = ['_' for i in word]
    tries = 0

    while tries < len(HANGMAN):
        print(term.clear)
        print('Długość słowa:', len(word))
        if wrong_lttrs:
            print(HANGMAN[tries])
            print('Wprowadzone litery: ', ' '.join(wrong_lttrs))
        print(' '.join(g_word).upper())
        guess = input('Wprowadź literę: ')

        # check if the guessed letter is in the key word
        if guess.lower()[0] not in word:
            tries += 1
            wrong_lttrs += guess.upper()[0]
        else:
            g_word = find_lttr(word, g_word, guess)
            if ''.join(g_word) == word:
                print(word.upper())
                print('WYGRAŁEŚ')
                break

    if tries == len(HANGMAN):
        print('RIP')
        print('Słowo klucz:', word.upper())

if __name__ == "__main__":
    main()
