from base_skill.skill import *


handler = CommandHandler()


@handler.hello_command
def hello(req, res, session):
    res.text = 'Привет, сыграем?'
    res.buttons = [button(txt) for txt in ('Да', 'Нет')]
    session['state'] = 0


@handler.command(words=('да', 'даа'), states=0)
def yes(req, res, session):
    res.text = 'Ну поехали'
    session['state'] = 1
    session['points'] = 0
    session['word'] = 'залупа'


@handler.command(words=('нет', 'не'), states=0)
def no(req, res, session):
    res.text = 'Ну как хочешь. Пока'
    session['state'] = 0
    res.end_session = True


@handler.undefined_command(states=1)
def play(req, res, session):
    tokens = req.tokens
    if session['word'] in tokens:
        res.text = 'Красава'
        session['points'] += 1
    else:
        res.text = 'Дебил'


@handler.undefined_command(states=0)
def wtf(req, res, session):
    res.text = 'Я не понимаю тебя'


class ZhopaSkill(BaseSkill):
    name = 'test_skill'
    command_handler = handler
