from googletrans import Translator

translator = Translator()


def translate_eng(string: str):
    result = translator.translate(string, dest='ru', src='en')
    return result.text


def translate_rus(string: str):
    result = translator.translate(string, dest='en', src='ru')
    return result.text

