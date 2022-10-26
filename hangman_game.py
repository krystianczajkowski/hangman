#!/usr/bin/python3

import socket
from random import choice
from time import sleep
from blessed import Terminal
from translate import translate_lang

term = Terminal()

HANGMAN = {
    7: r"""
     ____
    |/   |
    |   
    |    
    |    
    |    
    |
    |_____
    """,
    6: """
     ____
    |/   |
    |   (_)
    |    
    |    
    |    
    |
    |_____
    """,
    5: """
     ____
    |/   |
    |   (_)
    |    |
    |    |    
    |    
    |
    |_____
    """,
    4: """
     ____
    |/   |
    |   (_)
    |   \\|
    |    |
    |    
    |
    |_____
    """,
    3: """
     ____
    |/   |
    |   (_)
    |   \\|/
    |    |
    |    
    |
    |_____
    """,
    2: """
     ____
    |/   |
    |   (_)
    |   \\|/
    |    |
    |   / 
    |
    |_____
    """,
    1: """
     ____
    |/   |
    |   (_)
    |   \\|/
    |    |
    |   / \\
    |
    |_____
    """,
    0: """
     ____
    |/   |
    |   (_)
    |   /|\\
    |    |
    |   | |
    |
    |_____
    """,
}

SUPPORTED_LANGUAGES = ['english', 'polish']

def main():

    if check_internet():
        play_game(*translate_lang())
    else:
        print(f'{term.clear}{term.red2}No internet connection!{term.normal}')
        play_game(
            get_word(
                select_language(
                    input(
                        f"Choose your language: supported languages - {SUPPORTED_LANGUAGES} "
                    )
                )
            )
        )


def check_internet() -> bool:
    """Checks for internet conectivity"""
    return socket.gethostbyname(socket.gethostname()) != "127.0.0.1"


def select_language(lang: str) -> str:
    """Returns language if it's supported otherwise returns english"""

    if lang.lower() in SUPPORTED_LANGUAGES:
        return lang.lower()
    else:
        print(
            f"{term.red2}Language: {term.cornflowerblue}{lang}{term.red2} unsupported! Defaulting to English.{term.normal}"
        )
        return "english"


def get_word(language: str) -> str:
    """Grabs a random word with definition from a file"""
    with open(f"{language}.txt", encoding="utf-8") as f:
        return choice(f.readlines()).strip().lower()


def find_lttr(word: str, g_word: list, lttr: str) -> list | str:
    """Searches one string for a letter and if it finds it replaces it in second string(which is a list)."""
    if lttr.lower() == word:
        g_word = word
        return g_word
    elif len(lttr) > 1:
        lttr = lttr[0]
    for i, l in enumerate(word):
        if l == lttr:
            g_word[i] = word[i]
    return g_word


def play_game(word: str, word_with_definition: str) -> None:
    """Plays the game of hangman"""
    wrong_lttrs = ""
    # turn the word into a list and replace all letters with underscores, spaces stay where they are
    g_word = ["_" if i != " " else i for i in word]
    # number of spaces
    spaces = 0 + sum([1 for i in word if i == " "])
    # lenght of the word without spaces
    len_word = len(word) - spaces
    tries = len(HANGMAN)

    while tries > 0:
        print(term.clear)
        if spaces:
            print(
                f"{term.move_xy(2, 13)}Lenght of the word: {len_word}\n {term.move_xy(20, 14)}Number of spaces: {spaces}",
                end=" ",
            )
        else:
            print(f"{term.move_xy(2, 14)}Lenght of the word: {len_word}")

        if wrong_lttrs:
            print(f'{HANGMAN[tries]}')
            print(f'{term.move_xy(2, 12)}Entered letters: {" ".join(wrong_lttrs)}')

        print(f"{term.move_xy(20,15)}{' '.join(g_word).upper()}")
        guess = input(f"{term.move_xy(20, 20)}Enter a letter: ")
        # check if the first guessed letter is in the key word
        if guess and guess.lower()[0] not in word:
            tries -= 1
            wrong_lttrs += guess.upper()[0]
        else:
            g_word = find_lttr(word, g_word, guess)
            if "".join(g_word) == word:
                print(f"{term.move_xy(20, 14)}{' '.join(g_word).upper()}")
                print(
                    f"{term.green}CONGRATULATIONS\nThe word was {word.upper()}{term.normal}"
                )
                break

    if tries == 0:
        print(term.clear)
        print(f"{term.red2_on_black}{term.move_down(10)}{(HANGMAN[tries])}", " RIP")
        print(f'{term.center(f"Word was: {word}")}{term.normal}')
        sleep(4)
        print(f"{term.skyblue_on_black}{term.clear}")
        print(f"{term.move_xy(5, 5)}Press SPACE to play again or ESC to quit.")
        print(f'{term.move_xy(5, 7)}If you want to get the definition press "i".')
        print(f"{term.move_xy(5, 9)}Disclaimer all definitions are in English!")
        val = ""
        with term.cbreak():
            # wait for keypress
            while val.lower() != " ":
                val = term.inkey(timeout=10)
                if not val:
                    print(f"{term.clear}{term.move_xy(5, 10)}Press 'ESC' to quit, 'i' to get information about the word, 'SPACE' to play again.")
                elif val.name == "KEY_ESCAPE":
                    exit(f"{term.move_xy(5, 10)}{term.red2_on_black}BYE!{term.normal}")
                elif val.lower() == "i":
                    exit(f'{term.move_right(10)}{word_with_definition}')
            print(term.normal)
        if val == " ":
            main()


if __name__ == "__main__":
    main()
