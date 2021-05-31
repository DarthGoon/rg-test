"""
The HashProvider is a pluggable component that manages
the retrieval of hashes againse a store.

It takes a cypher funstion, and a dictionary store.

ex. hp = HashProvider(hashutil.sha256, redisutil.RedisStore)

This hash provider is written with a few assumptions.
The use cases are to retrieve a message by hash input,
and to retrieve a hash by message input.

To that end-- this is a _certain_ amount of code;
To accomplish a _certain_ amount of functionality;
While accepting a _certain_ amount of limitations.

The root of the problem is the performance of the cypher at
scale, and the trade-offs you can get away with, while still
accomplishing the goal.
The worst case is that you have large message. It is time
consuming to hash it, and you don't want to do that more
than once.
One way to not hash repeatedly-- is to store the text by hash,
and the hash by text, in a fast access storage layer. This
will eventually have it's own limitations, however.

There is currently a 255 char query string limit, enforced
by the API server. This is further explained in the server.py
file.  TL;DR- i don't want to end up with a $1000 cloud meter
this month.
In this scenario; we will never have a message large enough
to surpass the Redis key/value size limit (our next limitiation
using POST requests payloads), at 512MB

"""


class HashProvider():

    def __init__(self, cypher, store):
        '''
        Why is the cypher and store injected?
        - As a sha256 hashing service-- I feel the service
        orchestration layer should dictate the cypher.
        - The store may become a limitation, and should be
        swappable.
        - Makes the component more testable
        '''
        self.cypher = cypher
        self.store = store

    def getMessageByHash(self, hash):
        # we knew this part.
        return self.store.get(hash)

    def getHashByMessage(self, msg):
        # attempt to retrieve the hash by text
        hash = self.store.get(msg)
        if not hash:
            # hash our message
            hash = self.cypher(msg.encode()).hexdigest()
            # save the msg by hash, and hash by msg
            self.store.set(hash, msg)
            self.store.set(msg, hash)
        return hash
