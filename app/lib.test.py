from unittest import main, TestCase
from lib import HashProvider
from hashlib import sha256


mock_store = {}


class Mock_Rdb():
    def get(self, k):
        return mock_store[k]

    def set(self, k, v):
        mock_store[k] = v


class Test_Message_Hashing(TestCase):

    def setUp(self):
        self.hp = HashProvider(sha256, Mock_Rdb())
        self.msg = "I am a meat popsicle"
        self.hash = sha256(self.msg.encode()).hexdigest()

    def test_get_message(self):
        self.assertEqual(self.hp.getMessageByHash(self.hash), self.msg)

    def test_get_hash(self):
        self.assertEqual(self.hp.getHashByMessage(self.msg), self.hash)


if __name__ == '__main__':
    main()
