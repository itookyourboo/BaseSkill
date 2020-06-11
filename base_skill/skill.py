import datetime
import os
from abc import ABCMeta, abstractmethod


class BaseSkill:
    BASE_DIR = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1])
    __metaclass__ = ABCMeta

    def __init__(self):
        self.logger = None

    @property
    def name(self):
        assert NotImplementedError

    @property
    def command_handler(self):
        assert NotImplementedError

    def log(self, req, res, session):
        with open(f'{BaseSkill.BASE_DIR}/{self.name}_logs.txt', 'a') as file:
            file.write(f'\n{datetime.datetime.now()}\nUSR: {req.user_id[:5]}\nREQ: {req.text}\nRES: {res.text}\n'
                       f'------------------')


class Request:
    def __init__(self, req):
        self.req = req

    @property
    def has_screen(self):
        return 'screen' in self.req['meta']['interfaces']

    @property
    def new_session(self):
        return self.req['session']['new']

    @property
    def user_id(self):
        if 'user' in self.req['session']:
            return self.req['session']['user']['user_id']
        return self.req['session']['user_id']

    @property
    def app_id(self):
        return self.req['session']['application']['application_id']

    @property
    def text(self):
        if 'original_utterance' in self.req['request']:
            return self.req['request']['original_utterance']
        elif 'text' in self.req['request'].get('payload', {}):
            return self.req['request']['payload']['text']

    @property
    def tokens(self):
        return self.req['request']['nlu']['tokens']


class Response:
    def __init__(self, res):
        self.res = res

    @property
    def text(self):
        return self.res['response'].get('text', '')

    @text.setter
    def text(self, x):
        self.res['response']['text'] = x

    @property
    def tts(self):
        return self.res['response'].get('tts', self.text)

    @tts.setter
    def tts(self, x):
        self.res['response']['tts'] = x

    @property
    def buttons(self):
        return self.res['response'].get('buttons', [])

    @buttons.setter
    def buttons(self, x):
        self.res['response']['buttons'] = x

    @property
    def end_session(self):
        return self.res['response']['end_session']

    @end_session.setter
    def end_session(self, x):
        self.res['response']['end_session'] = x


def button(title='Title', hide=True, url=None):
    d = {
        'title': title,
        'hide': hide
    }
    if url is not None:
        d['url'] = url
    return d


class Command:
    def __init__(self, words=None, states=None, action=None):
        if words is not None:
            self.words = tuple(words)
        if states is not None:
            if isinstance(states, tuple):
                self.states = states
            else:
                self.states = (states,)
        if action is not None:
            self.action = action

    def execute(self, req, res, session):
        self.action()(req=req, res=res, session=session)


class CommandHandler:
    def __init__(self):
        self.commands = []
        self.undefined = []
        self.hello = None

    def execute(self, req, res, session):
        tokens = req.tokens
        executed = False
        for cmd in self.commands:
            if session['state'] not in cmd.states:
                continue
            if any(word in cmd.words for word in tokens):
                cmd.execute(req, res, session)
                executed = True
                break

        if not executed and len(self.undefined):
            for cmd in self.undefined:
                if session['state'] in cmd.states or cmd.states is None:
                    cmd.execute(req, res, session)
                    return

    def command(self, words, states):
        def decorator(func):
            def wrapped():
                return func

            self.commands.append(Command(words=words, states=states, action=wrapped))
            return wrapped

        return decorator

    def hello_command(self, action):
        def wrapped():
            return action

        self.hello = Command(action=wrapped)
        return wrapped

    def undefined_command(self, states):
        def decorator(func):
            def wrapped():
                return func

            self.undefined.append(Command(states=states, action=wrapped))
            return wrapped

        return decorator
