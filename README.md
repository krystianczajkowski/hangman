# UNIVERSAL HANGMAN
## *This is my final project for CS50P.*
-----
## Video Demo: [Done](https://youtu.be/opK-rbcFhpU)
-----
## Description:
## What's Universal Hangman? 

It's normal hangman but you can choose any language you want (*that is aslo coincidentally supported by Google Translate - more on that later*) and maybe a few other features that end user won't notice.

## How does it work?
It doesn't divagate too much from standard whiteboard/blackboard hangman everyone had a chance to play or at least spectate at some point in their lives. <br>
You will find [detailed description](#every-function-except-tests-in-the-project-is-located-here) bellow

## Structure:
## [project.py](project.py)
- ### Every function *(except tests)* in the project is located here.
    <details><summary>
    Details
    </summary><p>

    ### Description of the contents
    ###### <a href=https://take.quiz-maker.com/poll4550402x0DD34b61-142>Too many details?</a>

    <details><summary>Miscellaneous</summary><p>

    ### First iteration of the hangman just printed text on the screen
    ```python
    os.system('cls') # clearing the screen
    for i in range(5): # that's how space was created
        print()
    print(HANGMAN[tries])
    ```
    ### This was ugly, so the next step was to find a library that would solve this problem
    ### Curses library was the obvious first choice but after a bit of research Blessed was the final answer
    ```python
    from Blessed import Terminal

    #Initializes the terminal
    term = Terminal()
    print(term.clear+term.home) # clear the screen and place the cursor at the top-left corner of the screen
    
    ```
    ##### For more information check the <a href='https://pypi.org/project/blessed/'>PyPi</a>
    
    -----
    
    ## No internet
    ```python
    # in case of no internet connection, this list is used.
    SUPPORTED_LANGUAGES = ['english', 'polish']
    ```
    ## Storing the gallows...
    ```python
    # HANGMAN is a dictionary for storing the gallows
    # It's made out of int keys and string literals as values
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
    """, ...}
    ```
    </p></details>
    <details><summary>Main</summary><p>

    ## Main - Besides starting the program not much going on in there.
     
    ```python
    def main():
        print(f'{term.clear+term.home}') # make space on the screen
        print(pyfiglet.figlet_format('HANGMAN', font='cybermedium')) # print the title
        # check internet
        if check_internet():
        # begin online play
        play_game(*translate_lang())
        else:
        # start offline if check failed
        print(f'{term.clear}{term.red2}No internet connection!{term.normal}')
        play_game(
            get_word(
                select_language(
                    input(
                        f"Choose your language: supported languages - {SUPPORTED_LANGUAGES} "
                    )
                )# definitions for words are not available in offline mode because of their format and size
           ), 'Definition unavailable due to lack of internet!')
    ```
    </p></details>
     
    <details><summary>Checking for internet connection</summary><p>
    
    ## 📄 Docstring says it all!

    ```python
    def check_internet() -> bool:
        """Checks for network conectivity"""
        try:
            # try to get a response from google
            requests.get('https://translate.google.com')
            # on success
               return True
            except ConnectionError:
            # on failure
                return False
    ```
    </p></details>

    <details><summary>Selecting a language</summary><p>

    ## Does just that
    ##### *Only used if check for internet failed.

    ```python
    def select_language(lang: str) -> str:
        """Returns language if it's supported otherwise returns english"""
        if lang.lower() in SUPPORTED_LANGUAGES: # manually created list of languages
            return lang.lower()
        else:
            print(
                f"{term.red2}Language: {term.cornflowerblue}{lang}{term.red2} unsupported! Defaulting to English.{term.normal}")
            sleep(2) # let the user read the error message
            return "english"
    ```

    </p></details>
    <details><summary>Translating words</summary><p>

    ## Using <a href='https://pypi.org/project/deep-translator/#description'>deep_translator</a> to translate english to every language supported by the translator
    ### For the purpose of this game I've chosen Google Translate as it seemed unnecessary to complicate things with switching between multiple translators.
    ------

    ### Translate function first asks for input
    ```python
    language = input('Enter a language: ').lower()
    ```
    ### Then selects a random line from the file and separates word from it's definition
    ```python
    with open('words_with_definitions.txt', encoding='utf-8') as f:
        data = choice(f.readlines()).lower().split()
        word = data[0]
        definition = ' '.join(data[1:])
    ```
    ### Avoiding translating english to english 
    ```python
    if language == 'en' or language == 'english':
        return word, f'{word.upper()} - {definition}'
    ```
    ### Check if user provided any language
    ### If language is not supported return english version, otherwise return translated word with definition
    ```python
    else:
        try:
            if language:
                translated = GoogleTranslator(
                    source='en', target=language).translate(word)
            else:
                print('No language provided, defaulting to english!')
                sleep(1)
                return word, f'{word.upper()} - {definition}'

        except LanguageNotSupportedException:
            print(f'Language {language} not supported, swiched to english!')
            sleep(1)
            return word, f'{word.upper()} - {definition}'

        return translated, f'{word.upper()} - {definition}'
    ```
    </p></details>
    <details><summary>Selecting the word if there's no internet</summary><p>

    ### Gets the words in the same fashion as translate function.
    ##### *Only used if check for internet failed.
    ```python
    # doesn't have to check for language as it was already done by select_language
    def get_word(language: str) -> str:
    """Grabs a random word from a file"""
    with open(f"{language}.txt", encoding="utf-8") as f:
        return choice(f.readlines()).strip().lower()
    ```
    
    </p></details>
    <details><summary>Playing the game</summary><p>
    
    ### Now we can play the game
    ```python
    def play_game(word: str, word_with_definition: str) -> None:
    """Plays the game of hangman""" # documenting what this function does turned out to be harder that expected
    ```
    ### Before any loops, initialize a few variables
    
    ```python
    # imagine if all variables were named i, j, k, l, m, n, 🤯
    TITLE = pyfiglet.figlet_format("HANGMAN", font="banner3-D")
    wrong_lttrs, g_word = "", ["_" if letter != " " else letter for letter in word]
    spaces = 0 + sum([1 for i in word if i == " "])
    len_word = len(word) - spaces # number of letters
    num_of_words = len(word.split())
    tries = len(HANGMAN)
    ```
    ### Now time for loops
    ##### As far as I know it's not possible to get SIGWINCH(terminal resize signal) on Windows or the equivalent solution is not practical. [citation needed]
    ```python
    shown = False
    # loop forever
    while True:
        # this one is checks if the game will fit on the screen
        while term.height < 22 or term.width < 80:
            if not shown:
            # if the size is too small it will print the warninig
                print(
                f"{term.clear+term.home+term.cyan+term.move_xy(term.width//2-10, term.height//2)}Increase your terminal size!{term.red2}"
            , 'NOW!')
            sleep(0.15)
            shown = term.width > 22 and term.width > 80
        shown = False 
    ```
    ### After that is done it's time to draw the game
    ```python
    # clear the screen and draw the big hangman banner
    print(f"{term.normal+term.clear}{TITLE}")
    ```
    ```python
    # if spaces are present display how many are there
    if spaces:
        print(f"{term.move_xy(20, term.height//2-2)}Lenght of the word: {len_word}\n {term.move_xy(20, term.height//2-3)}Number of spaces: {spaces}",end=" ",)
        
        print(f"{term.move_xy(20, term.height//2+3)}Number of words: {num_of_words}")
    else: # if not print just the lenght
        print(f"{term.move_xy(20, term.height//2+2)}Lenght of the word: {len_word}")
    # if incorrect guesses were made display entered letters and state of the gallows
    if wrong_lttrs:
        print(f'{term.move_xy(20, term.height//2)}Entered letters: {" ".join(wrong_lttrs)}')
        print(f"{term.move_xy(0, term.height//2)}{HANGMAN[tries]}")
    
    ```
    ### Getting user input, displaying correctly guessed letters and handling succes
    ```python
    print(f"{term.move_xy(20, term.height//2+7)}{' '.join(g_word).upper()}")
    guess = input(f"{term.move_xy(20, term.height//2+8)}Enter a letter: {term.green}")
    
    # validating user input
    if guess and guess.lower()[0] not in word:
            tries -= 1
            wrong_lttrs += guess.upper()[0]
        
    else:
        # replace underscores in g_word with correctly guessed letters
        g_word = find_lttr(word, g_word, guess)
        # if all letters match the game is won
        if "".join(g_word) == word:
            print(f"{term.move_xy(20, term.height//2+6)}{' '.join(g_word).upper()}")
            print(f"{term.green+term.move_right(20)}Congratulations The word was {word.upper()}{term.normal}")
            # prompt to play again/see the definition of the word
            play_again_or_get_definition(word_with_definition)
    ```
    ### Game over state
    ```python
    if tries == 0:
        # clear the screen, draw the title in red
        print(f'{term.clear}{term.normal}{term.red2_on_black}{TITLE}')
        # draw the hangman on the gallows
        print(f"{term.red2_on_black}{term.move_xy(0, term.height//2)}{(HANGMAN[tries])}","RIP")
        # let the player know what was the word
        print(f"{term.move_xy(20, term.height//2+4)}Word: {word}")
        sleep(3) # give user time to read the word
        # prompt to play again/see the definition of the word
        play_again_or_get_definition(word_with_definition) 
    ```

    </p></details>
    <details><summary>Checking if user input matches the selected word</summary>
    <p>

    ### This is easily done. Since words will never get long enough for us to notice any performance drops, just loop through them each time.
    ```python
    # if user entered the whole word return the word
    if lttr.lower() == word:
        g_word = word
        return g_word
    # if letter is not a single character, consider only the first one
    elif len(lttr) > 1:
        lttr = lttr[0]
    # replace words where they match
    for i, l in enumerate(word):
        if l == lttr:
            g_word[i] = word[i]
    return g_word
    ```
    </p></details>
    

    <details><summary>Playing again</summary><p>

    ### First display some info
    ```python
    print(f"{term.skyblue}{term.move_right(20)}Press SPACE to play again or ESC to quit.")
    print(f'{term.move_right(20)}If you want to get the definition press "i".{term.normal}')
    ```
    ### Then prompt the user for input without the need to confirm it(pressing enter)
    ```python
    val = ""
    shown = False
    with term.cbreak():
        # wait for keypress
        while val.lower() != " ":
            val = term.inkey(timeout=20)
            if not val:
                # after 20 seconds display reminder for the user
                with term.location(0, 8):
                    print(
                        f"{term.red}Press 'ESC' to quit, 'i' to get the definition(EN) or 'SPACE' to play again.{term.normal}"
                    )
            # exit the program on Esc
            elif val.name == "KEY_ESCAPE":
                exit(
                    f"{term.clear}{term.move_xy(0 ,term.height//2)}{term.red_on_white(term.center('BYE!'))}{term.normal}{term.move_xy(0,term.height)}"
                )
            # diplay the definition once per game
            elif val.lower() == "i" and not shown:
                print(
                    f"{term.move_xy(20, term.height//2)+term.lightblue}{definition}{term.move_xy(0,term.height)+term.normal}"
                )
                shown = True
    ```
    ##### Why not use this in the play_game function? *~The anticipation...*
    ### When user decides to press SPACE
    ```python
    # clear the screen and call main so that we have come full circle back to the beginning
    if val == " ":
        print(term.clear + term.normal)
        main()
    ```
    ###### Thanks for coming to my tedx talk
    </p></details>
    </p></details>

## [Requirements](requirements.txt)

## [test_project.py](test_project.py)
- tests functions in project.py
- uses [test_language.txt](test_language.txt) for tests

### english/polish.txt
- these are files that contain words for offline play
- english.txt contains only 12 words (*guess which*)
- polish.txt has only slighty more at around 3 million words, taken from <a href='https://sjp.pl/sl/growy/'>sjp.pl</a>

### words_with_definitions.txt 
- around 300 thousand english words with definitions
