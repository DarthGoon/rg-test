from os import environ
from hashlib import sha256
from bottle import Bottle, run, request
from redis import Redis

app = Bottle()
rdb = Redis(host=environ.get('REDIS_HOST', 'redis'),
            port=environ.get('REDIS_PORT', '6379'),
            db=0)


@app.route('/')
def index():
    return 'Rigetti test API by Aaron Dayalan'


@app.get('/hash')
def hash():
    msg = request.query.msg
    hash = sha256(msg.encode()).hexdigest()
    rdb.set(hash, msg)
    return hash


@app.get('/message')
def message():
    msg = rdb.get(request.query.hash)
    return msg


if __name__ == '__main__':
    run(app,
        reloader=environ.get('RELOAD') == "True",
        host=environ.get('HOST', '0.0.0.0'),
        port=environ.get('PORT', 5000))
