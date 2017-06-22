import hashlib
import binascii
import os
import math

HASH_ALGORITHM = 'sha512'
HASHER = hashlib.new(HASH_ALGORITHM)

NONCE_SIZE = 8

DIFFICULTY_ORDER = 4
DIFFICULTY = math.pow(16, DIFFICULTY_ORDER)


class Block:
    def __init__(self, previous, data, nonce):
        self.previous = previous
        self.data = data
        self.nonce = nonce

        previous_hash = ''
        if self.previous is not None:
            previous_hash = self.previous.get_hash()
        HASHER.update(previous_hash+self.data+self.nonce)
        self.hash = HASHER.digest()

        if self.previous is None:
            self.height = 0
        else:
            self.height = self.previous.get_height()+1

    def get_previous(self):
        return self.previous

    def get_data(self):
        return self.data

    def get_nonce(self):
        return self.nonce

    def get_hash(self):
        return self.hash

    def get_hash_ascii(self):
        return binascii.hexlify(self.get_hash())

    def get_height(self):
        return self.height

    def get_string(self):
        return 'data %s,\theight %s,\thash %s' % (self.get_data(), self.get_height(), self.get_hash_ascii())


def mine_block(previous, data, difficulty_phrase='0'):

    while True:
        b = Block(previous, data, os.urandom(NONCE_SIZE))
        hash = b.get_hash_ascii()

        valid = True
        for i in range(0, DIFFICULTY_ORDER):
            if hash[i] is not '0':
                valid = False
                break

        if valid:
            return b