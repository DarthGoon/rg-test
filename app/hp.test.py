"""
HashProvider test suite
"""
from unittest import main, TestCase
from hp import HashProvider
from hashlib import sha256


# mock database store (generic dictionary)
mock_store = {}


class Mock_Rdb():
    '''
    This is a simple redis mock.  It simulates a
    key/value store adapter class.
    '''
    def get(self, k):
        return mock_store.get(k)

    def set(self, k, v):
        mock_store[k] = v


class Test_Message_Hashing(TestCase):

    def setUp(self):
        self.hp = HashProvider(sha256, Mock_Rdb())
        self.msg = "I am a meat popsicle"
        self.hash = sha256(self.msg.encode()).hexdigest()

    def test_get_hash_by_message(self):
        self.assertEqual(self.hp.getHashByMessage(self.msg), self.hash)

    def test_get_message_by_hash(self):
        self.assertEqual(self.hp.getMessageByHash(self.hash), self.msg)


if __name__ == '__main__':
    main()
