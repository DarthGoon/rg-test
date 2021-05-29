from os import environ
from lib import HashProvider
from hashlib import sha256
from bottle import Bottle, run, request, response
from redis import Redis

app = Bottle()
rdb = Redis(host=environ.get('REDIS_HOST'),
            port=environ.get('REDIS_PORT'),
            db=0)
hp = HashProvider(sha256, rdb)


@app.route('/')
def index():
    return 'Rigetti test API by Aaron Dayalan'


@app.get('/hash')
def hash():
    msg = request.query.get('msg')
    if not msg:
        return respond(400, 'missing "msg=" param')
    else:
        return hp.getHashByMessage(msg)


@app.get('/message')
def message():
    hash = request.query.get('hash')
    if not hash:
        return respond(400, 'missing "hash=" param')
    else:
        msg = hp.getMessageByHash(hash)
        if not msg:
            return respond(204)
        else:
            return msg


def respond(code, msg=None):
    response.status = code
    return msg


if __name__ == '__main__':
    run(app,
        reloader=environ.get('RELOAD') == "True",
        host=environ.get('HOST'),
        port=environ.get('PORT'))
