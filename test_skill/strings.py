from random import choice


TEXT_HELLO = 'Привет, сыграем?'
TEXT_PLAY = 'Ну, поехали/Погнали/Начинаем'
TEXT_WELL = 'Хорошо/Круто/Молодец'
TEXT_NO = 'Неа/Неправильно'
TEXT_WTF = 'Я не понимаю/Моя твоя не понимать'
TEXT_BYE = 'Пока!/До свидания!'

WORDS_YES = 'да/даа'
WORDS_NO = 'нет/неа/не'

BUTTONS_HELLO = 'Да', 'Нет'


def txt(string):
    return choice(string.split('/'))


def tkn(string):
    return tuple(string.split('/'))


def btn(string):
    if isinstance(string, tuple):
        return string
    return string,
