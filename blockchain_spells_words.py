import hashlib
import os
import math

# Import a custom encoding library
# The encode() function returns a base64 encoded string representing the contents of any
# binary data passed to the function
from encode import encode, encode_32

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
DIFFICULTY_ORDER = 4

# This is inverse of the probability of the output of an encoded hash being a 0
# Since hashes are encoded in base64, there is a 1/64 probability that any given character in the encoded hash is a 0
# This is used to estimate the difficulty of mining a block by the number of hashes required to find it.
# Suggested Value: 64
ENCODING_ORDER = 32

# Estimate the difficulty of mining a block in hashes using the encoding order and the difficulty order.
DIFFICULTY = math.pow(ENCODING_ORDER, DIFFICULTY_ORDER)

# The first DIFFICULTY_ORDER letters of the difficulty phrase will be spelled out in every single block
# This does not change the difficulty of mining blocks. It just tells the mining algorithm to search for specific
# words instead of 0s.
#
#
# The hash 0x40_timJB1Qn1gzNckyp1XU5UFhUAidhZB... might be found with a difficulty of 3
# The hash 0x40_timthebeaverckyp1XU5UFhUAidhZB... might be found with a difficulty of 12
# The hash 0x40_timthebeaver000p1XU5UFhUAidhZB... might be found with a difficulty of 15
#
# The difficulty phrase for will always be the length of the encoded hash output. Shorter phrases will be padded with 0s
#
# For instance, timthebeaver becomes timthebeaver000000....
#
# If the difficulty order exceeds the length of the phrase, the algorithm pads the phrase with 0s.
DIFFICULTY_PHRASE = 'timthebeaver'
hasher = hashlib.new(HASH_ALGORITHM)
for i in range(len(DIFFICULTY_PHRASE), len(encode_32(hasher.digest()))):
    DIFFICULTY_PHRASE += '0'


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


# Mines a block with a given previous block and data
#
# This proof of work (PoW) algorithm is a simplified version of Biocoin's PoW algorithm.
#
# To mine a block with the simplified bitcoin algorithm, a nonce must be found that satisfies the condition that a hash
# of block data, the previous block's hash, and the nonce must have a given number of leading 0's.
#
# In this mining algorithm, the 0's have been replaced with a difficulty phrase that allows blockchains to spell out
# words in a block.
#
# previous must be a Block or a None object.
# data must be a string
# difficulty_order must be an integer that refers to the number of leading zeros required in a block's hash
# difficulty_phrase must be a string of length greater than or equal to the length of a base64 encode sha512 hash
def mine_block(previous, data, difficulty_phrase=DIFFICULTY_PHRASE, difficulty_order=DIFFICULTY_ORDER):
    # Loop until a block is found. This algorithm could take an arbitrarily long amount of time
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
        for i in range(0, DIFFICULTY_ORDER):
            # Add 5 to the starting index because the hash has been prefixed with "0x40_"
            if hash[i+5] is not DIFFICULTY_PHRASE[i]:
                valid = False
                break

        # If the block has been determined to be valid, return it. The block has been mined.
        if valid:
            return b
