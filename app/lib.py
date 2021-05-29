

class HashProvider():

    def __init__(self, cypher, store):
        self.cypher = cypher
        self.store = store

    def getMessageByHash(self, hash):
        return self.store.get(hash)

    def getHashByMessage(self, msg):
        hash = self.cypher(msg.encode()).hexdigest()
        self.store.set(hash, msg)
        return hash
