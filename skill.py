import logging
from abc import ABCMeta, abstractmethod


class BaseSkill:
    __metaclass__ = ABCMeta

    @property
    def name(self):
        assert NotImplementedError

    @property
    def url(self):
        assert NotImplementedError

    @property
    def log_path(self):
        assert NotImplementedError

    @property
    def command_handler(self):
        assert NotImplementedError

    def logger(self):
        if self.name is None:
            assert NotImplementedError("method 'name' isn't implemented")
            return
        if self.log_path is None:
            assert NotImplementedError("method 'log_path' isn't implemented")
            return
        logger = logging.getLogger(self.name)
        handler = logging.FileHandler(self.log_path)
        handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        return logger

    def log(self, req, res, session):
        user_id, original_utterance = CommandHandler.get_from_req(req, want=('user_id', 'original_utterance'))
        original_utterance = req.get('request', {}).get('original_utterance', 'Empty request')
        self.logger().info(f"\n"
                            f"USR: {user_id[:5]}\n"
                            f"REQ: {original_utterance}\n"
                            f"RES: {res['response']['text']}\n"
                            f"----------------------")


class Command:
    def __init__(self, words=None, states=None, action=None):
        if words:
            self.words = tuple(words)
        if states:
            self.states = tuple(states)
        if action:
            self.action = action

    def execute(self, req, res, session):
        self.action(req, res, session)


class CommandHandler:
    def __init__(self):
        self.commands = []
        self.undefined = None
        self.hello = None

    def execute(self, req, res, session):
        tokens = req['request']['nlu']['tokens']
        executed = False
        for cmd in self.commands:
            if session['state'] not in cmd.states:
                continue
            if any(word in cmd.words for word in tokens):
                cmd.execute(req, res, session)
                executed = True
                break

        if not executed and self.undefined:
            self.undefined.action()

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

    def undefined_command(self, action):
        def wrapped():
            return action
        self.undefined = Command(action=action)
        return wrapped

    @staticmethod
    def get_from_req(req, want):
        result = []
        for w in want:
            if w == 'user_id':
                result.append(req['request']['user']['user_id'])
            elif w == 'tokens':
                result.append(req['request']['nlu']['tokens'])
            elif w == 'original_utterance':
                result.append(req['request']['original_utterance'])
            else:
                result.append('Добавь обработку')
        return result
