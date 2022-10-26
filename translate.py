
from deep_translator.exceptions import LanguageNotSupportedException
from deep_translator import GoogleTranslator
from random import choice
from time import sleep


def translate_lang():
    """Returns a random word translated to user specified language"""
    # specify lang
    language = input('Enter a language: ').lower()
    # grab a word
    with open('words_with_definitions.txt', encoding='utf-8') as f:
        data = choice(f.readlines()).lower().split()
        word = data[0]
        definition = ' '.join(data[1:])
    # don't translate from en to en
    if language == 'en' or language == 'english':
        return word, f'{word} - {definition}'
    else:
        try:
            # check if user pressed something besides enter
            if language:
                translated = GoogleTranslator(
                    source='en', target=language).translate(word)
            else:
                print('No language provided, defaulting to english!')
                sleep(1)
                return word, f'{word} - {definition}'

        except LanguageNotSupportedException:
            print('Language not supported, swiched to english!')
            sleep(1)
            return word, f'{word} - {definition}'

        return translated, f'{word} - {definition}'
