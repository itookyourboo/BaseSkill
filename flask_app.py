import json
import logging
from flask import Flask, request
from base_skill.skill import Response, Request
from test_skill.main import ZhopaSkill


app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('errors.txt'))
logger.setLevel(logging.ERROR)


zhopa = ZhopaSkill()
sessionStorage = {
    zhopa.name: {}
}


@app.route(zhopa.url, methods=['POST'])
def main():
    req = request.json
    return handle_dialog(req, zhopa)


def prepare_res(req):
    return {
        'session': req['session'],
        'version': req['version'],
        'response': {
            'end_session': False
        }
    }


def block_ping(req, res):
    if req.get('request', {}).get('original_utterance', '') == 'ping':
        res['response']['text'] = 'Всё работает!'
        return True
    return False


def get_user_id(req):
    return req['session']['user_id']


def handle_dialog(req, skill):
    try:
        res = prepare_res(req)
        session = sessionStorage[skill.name]
        user_id = get_user_id(req)

        if not block_ping(req, res):
            if req['session']['new']:
                session[user_id] = {'state': 0}
                skill.command_handler.hello.execute(req=Request(req), res=Response(res), session=session[user_id])
            else:
                if user_id not in session:
                    session[user_id] = {'state': 0}
                skill.command_handler.execute(req=Request(req), res=Response(res), session=session[user_id])

            skill.log(req=Request(req), res=Response(res), session=session)
        return json.dumps(res)
    except Exception as e:
        logger.error(f'{skill.name}: {e}')
        return {}
