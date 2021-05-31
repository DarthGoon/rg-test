"""
This is the server API orchestration.
It contains non business logic relavent to our functional
requirements, and all dependency configs values are stored
in env vars.

The requirement for this API is to allow a user to
retrieve messages and hashes.

Hashing is a complex operation, which increases in
duration, according to the amount of data. To the machine
this means a lot of CPU resources. For a service, this
also amounts to a lot of storage for messages. And for
the API, that means large payload requests.

All of which amount to CPU, storage, and network meter
charges in my personal gcloud...

This API purposely has a a message limit.
That limit is the 255 chars of a query string, in a GET
request.
255 chars will still take a few seconds to hash. It is
still possible to hammer that endpoint and run up a bill.

But I have monitoring, and I'm watching.
"""
from os import environ
from hp import HashProvider
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
    '''
    @app.post this endpoint to take a large message
    payload in the request.body; If requirements
    evolve to specify, or this service gets funding.
    '''
    hash = request.query.get('hash')
    if not hash:
        return respond(400, 'missing "hash=" param')
    else:
        msg = hp.getMessageByHash(hash)
        # user may input wrong hash
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
