#!/usr/bin/python3

import socket
from random import choice
from time import sleep
from blessed import Terminal
from translate import translate_lang
import pyfiglet

term = Terminal()
HANGMAN = {
    7: """
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

# in case of no internet use this
SUPPORTED_LANGUAGES = ['english', 'polish']
TITLE = pyfiglet.figlet_format('HANGMAN', font='banner3-D')


def main():
    print(f'{term.clear+term.home}')
    print(pyfiglet.figlet_format('HANGMAN', font='cybermedium'))
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
            ), 'Definition unavailable due to lack of internet!')

def check_internet() -> bool:
    """Checks for network conectivity(poorly)"""
    try:
        pass
    except:
        pass
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


def play_again_or_get_definition(definition):
    """Prompts the user to press a key."""
    print(
        f"{term.skyblue_on_black}{term.move_right(20)}Press SPACE to play again or ESC to quit.")
    print(
        f'{term.move_right(20)}If you want to get the definition press "i".{term.normal}')
    val = ""
    with term.cbreak():
        # wait for keypress
        while val.lower() != " ":
            val = term.inkey(timeout=20)
            if not val:
                with term.location(0, 8):
                    print(
                        f"{term.red}Press 'ESC' to quit, 'i' to get the definition(EN) or 'SPACE' to play again.{term.normal}")
            elif val.name == "KEY_ESCAPE":
                exit(
                    f"{term.clear}{term.move_xy(0 ,term.height//2)}{term.red_on_white(term.center('BYE!'))}{term.normal}{term.move_xy(0,term.height)}")
            elif val.lower() == "i":
                print(
                    f'{term.move_xy(20, term.height//2)+term.blue}{definition}{term.move_xy(0,term.height)+term.normal}')
    if val == " ":
        print(term.clear+term.normal)
        main()


def play_game(word: str, word_with_definition: str) -> None:
    """Plays the game of hangman"""

    wrong_lttrs, g_word = '', ["_" if letter !=
                               " " else letter for letter in word]
    spaces = 0 + sum([1 for i in word if i == " "])
    len_word = len(word) - spaces
    num_of_words = len(word.split())
    tries = len(HANGMAN)
    print(term.clear)
    while tries > -1:
        while term.height < 22 or term.width < 80:
            print(
                f'{term.clear+term.home+term.cyan+term.move_xy(0, term.height//2)}Increase your terminal size!{term.red2}')
            sleep(0.05)
        print(f'{term.normal+term.clear}{TITLE}')
        if spaces:
            print(
                f"{term.move_xy(20, term.height//2-2)}Lenght of the word: {len_word}\n {term.move_xy(20, term.height//2-3)}Number of spaces: {spaces}",
                end=" ",
            )
        else:
            print(f"{term.move_xy(20, term.height//2+2)}Lenght of the word: {len_word}")
            print(f"{term.move_xy(20, term.height//2+3)}Number of words: {num_of_words}")

        if wrong_lttrs:
            # stage of the fellow on the gallows
            print(
                f'{term.move_xy(20, term.height//2)}Entered letters: {" ".join(wrong_lttrs)}')
            print(f'{term.move_xy(0, term.height//2)}{HANGMAN[tries]}')

        print(f"{term.move_xy(20, term.height//2+7)}{' '.join(g_word).upper()}")
        # guess is happening here
        guess = input(f"{term.move_xy(20, term.height//2+8)}Enter a letter: {term.green}")
        if guess and guess.lower()[0] not in word:
            tries -= 1
            wrong_lttrs += guess.upper()[0]
        else:
            g_word = find_lttr(word, g_word, guess)
            if "".join(g_word) == word:
                print(
                    f"{term.move_xy(20, term.height//2+6)}{' '.join(g_word).upper()}")
                print(
                    f"{term.green+term.move_right(20)}CONGRATULATIONS The word was {word.upper()}{term.normal}"
                )
                play_again_or_get_definition(word_with_definition)

        if tries == 0:
            print(term.clear+term.normal)
            print(TITLE)
            print(
                f"{term.red2_on_black}{term.move_xy(0, term.height//2)}{(HANGMAN[tries])}", " RIP")
            print(f"{term.move_xy(20, term.height//2+4)}Word: {word}")
            sleep(3)
            play_again_or_get_definition(word_with_definition)


if __name__ == "__main__":
    main()
