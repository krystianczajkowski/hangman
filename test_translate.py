def translate_lang():
    from random import choice
    from deep_translator import GoogleTranslator
    language = input('language: ').lower()
    with open('words_with_definitions.txt', encoding='utf-8') as f:
        data = choice(f.readlines()).lower().split()
        word = data[0]
        definition = ' '.join(data[1:])
        
    if language == 'en' or language == 'english':
        return word, definition
    else:
        translated = GoogleTranslator(source='en', target=language).translate(word)
        return translated, (f'word: {word}, definition : {definition}')
