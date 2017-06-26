import hashlib
import os
import math

# Import a custom encoding library
# The encode() function returns a base64 encoded string representing the contents of any
# binary data passed to the function
from encode import encode

# Select the hashing algorithm to be passed to hashlib.new()
# SHA512 was selected due to its low probability of collision even when compared to other hasing algorithms
# Suggested Value: 'sha512'
HASH_ALGORITHM = 'sha512'

# The amount of random information to pull from os.urandom() in bytes for the nonce of each block
# Suggested Value: 8
NONCE_SIZE = 8


# The difficulty of the block is determined by how many leading figure must be 0s
# A difficulty order of 2 corresponds to hashes of blocks needing 2 leading 0s to be considered valid.
# The hash 0x40_000JB1Qn1gzNckyp1XU5UFhUAidhZB... is valid for a difficulty of 3 or less
# The hash 0x40_00AJB1Qn1gzNckyp1XU5UFhUAidhZB... is valid for a difficulty of 2 or less
# Suggested Value for Demos: 3
# Suggested Value for Production would be based on network hash rate: 3
DIFFICULTY_ORDER = 3

# This is inverse of the probability of the output of an encoded hash being a 0
# Since hashes are encoded in base64, there is a 1/64 probability that any given character in the encoded hash is a 0
# This is used to estimate the difficulty of mining a block by the number of hashes required to find it.
# Suggested Value: 64
ENCODING_ORDER = 64

# Estimate the difficulty of mining a block in hashes using the encoding order and the difficulty order.
DIFFICULTY = math.pow(ENCODING_ORDER, DIFFICULTY_ORDER)


# The block class is intended to store all associated block data in one place.
# It is not intended to create or 'mine' blocks. For this, use mine_block()
class Block:
    # Instantiate the blobk
    # The block height and block hash are computed from the input values.
    def __init__(self, previous, data, nonce):
        self.previous = previous
        self.data = data
        self.nonce = nonce

        previous_hash = ''
        if self.previous is not None:
            previous_hash = self.previous.get_hash()
        hasher = hashlib.new(HASH_ALGORITHM)
        hasher.update(previous_hash + self.data + self.nonce)
        self.hash = hasher.digest()

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
        return encode(self.get_hash())

    def get_height(self):
        return self.height

    def get_string(self):
        previous_hash = 'None'
        prev = self.get_previous()
        if prev is not None:
            previous_hash = prev.get_hash_encoded()
        return '----------block %s----------\nnonce %s\nprev %s\ndata\n----------\n%s\n----------\nhash %s\n----------End Block----------'\
               % (self.get_height(), self.get_nonce_encoded(), previous_hash, self.get_data(), self.get_hash_encoded())


# Mines a block with a given previous block and data
#
# This proof of work (PoW) algorithm is a simplified version of Biocoin's PoW algorithm.
#
# To mine a block, a nonce must be found that satisfies the condition that a hash of block data, the previous block's
# hash, and the nonce must have a given number of leading 0's.
#
# previous must be a Block or a None object.
# data must be a string
# difficulty_order must be an integer that refers to the number of leading zeros required in a block's hash
def mine_block(previous, data, difficulty_order=DIFFICULTY_ORDER):
    # Loop until a block is found. This algorithm could take an arbitratily long amount of time
    while True:
        # Generate a block based on the previous and the provided data with a random nonce
        b = Block(previous, data, os.urandom(NONCE_SIZE))

        # Fetch the base64 encoded version of the hash. This will be prefixed with the 5 character string "0x40_"
        # This is because the encode module offers both base64 and base32 hashing, and the goal of the module was
        # to provide clear, easy to use encodings. As a result, it is very easy to determine if an encoded string
        # is base64 or base32. 0x40 is 64 in hex. 0x20 is used for base 32.\
        # For instance, a valid hash may look like this: 0x40_000JB1Qn1gzNckyp1XU... Only the "000JB1Qn1gzNckyp1XU" is
        # base64 encoded data. "0x40_" is a prefix.
        hash = b.get_hash_encoded()

        # Assume that the block hash is valid according to the difficulty rules
        valid = True

        # Check in order if each character up to the desired difficulty level is a 0.
        # If it isn't, the nonce does not generate a valid hash, and we must try again with a new nonce
        # on the next iteration.
        for i in range(0, difficulty_order):
            # Add 5 to the starting index because the hash has been prefixed with "0x40_"
            if hash[i+5] is not '0':
                valid = False
                break

        # If the block has been determined to be valid, return it. The block has been mined.
        if valid:
            return b
