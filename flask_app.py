import json
from flask import Flask, request
from test_skill.main import ZhopaSkill


app = Flask(__name__)

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
    res = prepare_res(req)
    session = sessionStorage[skill.name]
    user_id = get_user_id(req)

    if not block_ping(req, res):
        if req['session']['new']:
            session[user_id] = {'state': 0}
            skill.command_handler.hello.execute(req=req, res=res, session=session[user_id])
        else:
            if user_id not in session:
                session[user_id] = {'state': 0}
            skill.command_handler.execute(req=req, res=res, session=session[user_id])

        skill.log(req=req, res=res, session=session)
    return json.dumps(res)
