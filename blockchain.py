import hashlib
import images
import math

from encode import encode, decode, encode_32, decode_32

HASH_ALGORITHM = 'sha512'
HASHER = hashlib.new(HASH_ALGORITHM)

NONCE_SIZE = 8

DIFFICULTY_ORDER = 1
ENCODING_ORDER = 32
DIFFICULTY = math.pow(ENCODING_ORDER, DIFFICULTY_ORDER)

DIFFICULTY_PHRASE = 'dankmemes'
for i in range(len(DIFFICULTY_PHRASE),len(encode(HASHER.digest()))):
    DIFFICULTY_PHRASE += '0'

def hash_block(previous_hash, data, nonce):
        HASHER.update(previous_hash + data + nonce)
        return HASHER.digest()


class Block:
    def __init__(self, previous_hash, height, data, nonce, reward_address):
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = nonce
        self.height = height

        self.hash = hash_block(self.previous_hash,self.data,self.nonce)

        self.reward_address = reward_address

    def get_previous_hash(self):
        return self.previous_hash

    def get_previous_hash_encoded(self):
        return encode_32(self.previous_hash)

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

    def get_reward_address(self):
        return self.reward_address

    def is_valid(self):
        if self.hash != hash_block(self.get_previous_hash(), self.data, self.nonce):
            return False

    def get_string(self):
        return '----------block %s----------\nnonce %s\nprev %s\nreward_address %s\n---data---\n%s\n----------\nhash %s\n----------End Block----------'\
               % (self.get_height(), self.get_nonce_encoded(), self.get_previous_hash_encoded(), self.get_reward_address(), self.get_data(), self.get_hash_encoded())


def mine_block(previous_hash, height, data, nonce_source, reward_address):
    while True:
        nonce = nonce_source.provide_nonce()

        # print "trying nonce %s" % encode(nonce)

        b = Block(previous_hash, height, data, nonce, reward_address)
        hash = b.get_hash_encoded()

        # print "got hash %s" % hash

        valid = True
        for i in range(0, DIFFICULTY_ORDER):
            if hash[i+5] is not DIFFICULTY_PHRASE[i]:
                valid = False
                break

        if valid:
            return b