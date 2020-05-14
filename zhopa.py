from skill import BaseSkill, CommandHandler, Command


handler = CommandHandler()


@handler.hello_command
def hello(req, res, session):
    res['response']['text'] = 'Привет, сыграем?'


@handler.command(words=('да', 'даа'), states=0)
def yes(req, res, session):
    res['response']['text'] = 'Ну поехали'
    session['state'] = 1
    session['points'] = 0
    session['word'] = 'Залупа'


@handler.command(words=('нет', 'не'), states=0)
def no(req, res, session):
    res['response']['text'] = 'Ну как хочешь. Пока'
    session['state'] = 0
    res['session']['end_session'] = True


@handler.undefined_command
def undef(req, res, session):
    if session['state'] == 0:
        res['response']['text'] = 'Я не понимаю тебя'
    else:
        user_id, tokens = CommandHandler.get_from_req(req, ('user_id', 'tokens'))
        if 'залупа' in tokens:
            res['response']['text'] = 'Красава'
            session['points'] += 1
        else:
            res['response']['text'] = 'Дебил'


class ZhopaSkill(BaseSkill):
    name = 'zhopa'
    url = '/zhopa'
    log_path = 'log/logs.txt'
    command_handler = handler
