from base_skill.skill import *
from .state import State
from .strings import *


handler = CommandHandler()


@handler.hello_command
def hello(req, res, session):
    res.text = txt(TEXT_HELLO)
    res.buttons = [button(x) for x in btn(BUTTONS_HELLO)]
    session['state'] = State.HELLO


@handler.command(words=tkn(WORDS_YES), states=State.HELLO)
def yes(req, res, session):
    res.text = txt(TEXT_PLAY)
    session['state'] = 1
    session['points'] = 0
    session['word'] = 'слово'


@handler.command(words=tkn(WORDS_NO), states=State.HELLO)
def no(req, res, session):
    res.text = txt(TEXT_BYE)
    session['state'] = State.HELLO
    res.end_session = True


@handler.undefined_command(states=State.PLAY)
def play(req, res, session):
    tokens = req.tokens
    if session['word'] in tokens:
        res.text = txt(TEXT_WELL)
        session['points'] += 1
    else:
        res.text = txt(TEXT_NO)


@handler.undefined_command(states=State.HELLO)
def hello_wtf(req, res, session):
    res.text = txt(TEXT_WTF)


@handler.undefined_command(states=tuple(State))
def wtf(req, res, session):
    # Catch something
    pass


class TestSkill(BaseSkill):
    name = 'test_skill'
    command_handler = handler
