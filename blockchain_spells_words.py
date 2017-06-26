import hashlib
import os
import math

from encode import encode, decode, encode_32, decode_32

HASH_ALGORITHM = 'sha512'
HASHER = hashlib.new(HASH_ALGORITHM)

NONCE_SIZE = 8

DIFFICULTY_ORDER = 4
ENCODING_ORDER = 32
DIFFICULTY = math.pow(ENCODING_ORDER, DIFFICULTY_ORDER)

DIFFICULTY_PHRASE = 'timthebeaver'
for i in range(len(DIFFICULTY_PHRASE),len(encode(HASHER.digest()))):
    DIFFICULTY_PHRASE += '0'


class Block:
    def __init__(self, previous, data, nonce):
        self.previous = previous
        self.data = data
        self.nonce = nonce

        previous_hash = ''
        if self.previous is not None:
            previous_hash = self.previous.get_hash()
        HASHER.update(previous_hash + self.data + self.nonce)
        self.hash = HASHER.digest()

        if self.previous is None:
            self.height = 0
        else:
            self.height = self.previous.get_height() + 1

    def get_previous(self):
        return self.previous

    def get_data(self):
        return self.data

    def get_nonce(self):
        return self.nonce

    def get_nonce_encoded(self):
        return encode(self.nonce)

    def get_hash(self):
        return self.hash

    def get_hash_encoded(self):
        return encode_32(self.get_hash())

    def get_height(self):
        return self.height

    def get_string(self):
        previous_hash = 'None'
        prev = self.get_previous()
        if prev is not None:
            previous_hash = prev.get_hash_encoded()
        return '----------block %s----------\nnonce %s\nprev %s\ndata\n----------\n%s\n----------\nhash %s\n----------End Block----------'\
               % (self.get_height(), self.get_nonce_encoded(), previous_hash, self.get_data(), self.get_hash_encoded())


def mine_block(previous, data, difficulty_phrase='0'):
    while True:
        b = Block(previous, data, os.urandom(NONCE_SIZE))
        hash = b.get_hash_encoded()

        valid = True
        for i in range(0, DIFFICULTY_ORDER):
            if hash[i+5] is not DIFFICULTY_PHRASE[i]:
                valid = False
                break

        if valid:
            return b
