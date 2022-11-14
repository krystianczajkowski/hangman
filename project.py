#!/usr/bin/python3

from blessed import Terminal
from deep_translator.exceptions import LanguageNotSupportedException
from deep_translator import GoogleTranslator
from requests.exceptions import ConnectionError
import requests
from random import choice
from time import sleep
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
SUPPORTED_LANGUAGES = ["english", "polish"]


def main():
    print(f"{term.clear+term.home}")
    print(pyfiglet.figlet_format("HANGMAN", font="cybermedium"))
    if check_internet():
        play_game(*translate())
    else:
        print(f"{term.clear}{term.red2}No internet connection!{term.normal}")
        play_game(
            get_word(
                select_language(
                    input(
                        f"Choose your language: supported languages - {SUPPORTED_LANGUAGES} "
                    )
                )
            ),
            "Definition unavailable due to lack of internet!",
        )


def check_internet() -> bool:
    """Checks for network conectivity"""
    try:
        return requests.get("https://translate.google.com")
    except ConnectionError:
        return False


def select_language(lang: str) -> str:
    """Returns language if it's supported otherwise returns english"""

    if lang.lower() in SUPPORTED_LANGUAGES:
        return lang.lower()
    else:
        print(
            f"{term.red2}Language: {term.cornflowerblue}{lang}{term.red2} unsupported! Defaulting to English.{term.normal}"
        )
        sleep(2)
        return "english"


def translate() -> tuple[str, str]:
    """Returns a random word from a file translated to user specified language"""
    # specify lang
    language = input("Enter a language: ").lower()
    # grab a word
    with open("words_with_definitions.txt", encoding="utf-8") as f:
        data = choice(f.readlines()).lower().split()
        word = data[0]
        definition = " ".join(data[1:])
    # don't translate from en to en
    if language == "en" or language == "english":
        return word, f"{word.upper()} - {definition}"
    else:
        try:
            if language:
                translated = GoogleTranslator(source="en", target=language).translate(
                    word
                )
            else:
                print("No language provided, defaulting to english!")
                sleep(1)
                return word, f"{word.upper()} - {definition}"

        except LanguageNotSupportedException:
            print(f"Language {language} not supported, swiched to english!")
            sleep(1)
            return word, f"{word.upper()} - {definition}"

        return translated, f"{word.upper()} - {definition}"


def get_word(language: str) -> str:
    """Grabs a random word from a file"""
    with open(f"{language}.txt", encoding="utf-8") as f:
        return choice(f.readlines()).strip().lower()


def find_lttr(word: str, g_word: list, lttr: str) -> list | str:
    """Searches word: str for a lttr: str|char and if it finds it, replaces it in g_word: list."""
    if lttr.lower() == word:
        g_word = word
        return g_word
    elif len(lttr) > 1:
        lttr = lttr[0]
    for i, l in enumerate(word):
        if l == lttr:
            g_word[i] = word[i]
    return g_word


def play_again_or_get_definition(definition: str):
    """Prompts the user to press a key."""
    print(
        f"{term.skyblue}{term.move_right(20)}Press SPACE to play again or ESC to quit."
    )
    print(
        f'{term.move_right(20)}If you want to get the definition press "i".{term.normal}'
    )
    val = ""
    shown = False
    with term.cbreak():
        # wait for keypress
        while val.lower() != " ":
            val = term.inkey(timeout=20)
            if not val:
                with term.location(0, 8):
                    print(
                        f"{term.red}Press 'ESC' to quit, 'i' to get the definition(EN) or 'SPACE' to play again.{term.normal}"
                    )
            elif val.name == "KEY_ESCAPE":
                exit(
                    f"{term.clear}{term.move_xy(0 ,term.height//2+1)}{term.red_on_white(term.center('BYE!'))}{term.normal}{term.move_xy(0,term.height)}"
                )
            elif val.lower() == "i" and not shown:
                with term.location(20, term.height//2):
                    print(
                        f"{term.lightblue}{definition}{term.normal}"
                    )
                shown = True
    if val == " ":
        main()


def play_game(word: str, word_with_definition: str) -> None:
    """Plays the game of hangman"""

    TITLE = pyfiglet.figlet_format("HANGMAN", font="banner3-D")
    wrong_lttrs, g_word = "", ["_" if letter != " " else letter for letter in word]
    spaces = 0 + sum([1 for i in word if i == " "])
    len_word = len(word) - spaces
    num_of_words = len(word.split())
    tries = len(HANGMAN)
    shown = False
    with term.cbreak(), term.hidden_cursor():
        while True:
            guess = ''
            while term.height < 22 or term.width < 80:
                if not shown:
                    print(
                        f"{term.clear+term.home+term.cyan+term.move_xy(term.width//2-10, term.height//2)}Increase your terminal size!{term.red2}",
                        "NOW!",
                    )
                sleep(0.15)
                shown = term.width > 22 and term.width > 80
            shown = False
            print(f"{term.normal+term.clear+term.home}{TITLE}")

            if spaces:
                print(
                    f"{term.move_xy(20, term.height//2-2)}Lenght of the word: {len_word}\n {term.move_xy(20, term.height//2-3)}Number of spaces: {spaces}",
                    end=" ",
                )
                print(
                    f"{term.move_xy(20, term.height//2+3)}Number of words: {num_of_words}"
                )
            else:
                print(
                    f"{term.move_xy(20, term.height//2+2)}Lenght of the word: {len_word}")

            if wrong_lttrs:
                # stage of the fellow on the gallows
                print(
                    f'{term.move_xy(20, term.height//2)}Entered letters: {" ".join(wrong_lttrs)}'
                )
                print(f"{term.move_xy(0, term.height//2)}{HANGMAN[tries]}")

            print(f"{term.move_xy(20, term.height//2+7)}{' '.join(g_word).upper()}")

            guess = term.inkey(timeout=30)
            if guess.name == "KEY_ESCAPE":
                exit(
                    f"{term.clear}{term.move_xy(0 ,term.height//2)}{term.red_on_white(term.center('BYE!'))}{term.normal}{term.move_xy(0,term.height)}"
                )
            elif str(guess).lower() not in word and str(guess).isalpha():
                tries -= 1
                wrong_lttrs += str(guess).upper()
            else:
                g_word = find_lttr(word, g_word, str(guess))
                if "".join(g_word) == word:
                    print(
                        f"{term.move_xy(20, term.height//2+6)}{' '.join(g_word).upper()}")
                    print(
                        f"{term.green+term.move_right(20)}Congratulations The word was {word.upper()}{term.normal}"
                    )
                    break
            if tries == 0:
                print(f'{term.clear}{term.normal}{term.red2_on_black}{TITLE}')
                print(
                    f"{term.red2_on_black}{term.move_xy(0, term.height//2)}{(HANGMAN[tries])}",
                    " RIP",
                )
                print(f"{term.move_xy(20, term.height//2+4)}Word: {word}")
                sleep(3)
                break
            
    play_again_or_get_definition(word_with_definition)


if __name__ == "__main__":
    main()
