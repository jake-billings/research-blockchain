import os
from encode import encode
from Crypto.PublicKey import RSA
import hashlib

# Select the hashing algorithm to be passed to hashlib.new()
# SHA224 was selected due to its shorter length and therefore higher convenience. It also maintains a very low
# probability of of collision.
# Suggested Value: 'sha224'
HASH_ALGORITHM = 'sha224'

# RSA key size for signatures
# A 1024 bit key size was selected for demos due to its quick generation time; for production blockchains, 2048 bit keys
# should be used to mitigate attacks from future increases in compute power.
KEY_SIZE = 1024

# Entropy source for key generation
# os.urandom was selected based on the python documentation's recommendation for cryptographic entropy sources
ENTROPY = os.urandom


# Generate an RSA key using a given key size and entropy
# This function just wraps RSA.generate()
#
# key_size must be an integer that meets the requirements in the PyCrypto docs for key sizes (Must be a multiple of 2
# that is greater than 1024).
# entropy must be a function that returns random bytes; similar to os.urandom
def generate_key(key_size=KEY_SIZE, entropy=ENTROPY):
    return RSA.generate(key_size, entropy)


# Convert a PyCrypto key to a base64 encoded string using the encode module
def key_to_string(key):
    return encode(key.exportKey(format="DER"))


# Sign a string using a PyCrypto key
#
# Returns an encoded string using the encode module representing the signature of the data using the key
#
# key must be a PyCrypto key
# data must be a string to be signed
def sign(key, data):
    return encode(key.sign(data, '')[0])


# Verifies a piece of data was signed with a given key
#
# Returns a boolean representing whether a signature is valid for a piece of data and a key
#
#
# key must be a PyCrypto key
# signature must be signature of the data
# data must be the string supposedly signed
def verify(key, signature, data):
    return key.verify(data, signature, None)


# Converts a PyCrypto key to an address
#
# Addresses are defined as the sha224 hash of a public key enocoded with base64
# using the encode module.
#
# key must be a PyCrypto key
def public_key_to_address(key):
    hasher = hashlib.new(HASH_ALGORITHM)
    hasher.update(key.exportKey(format="DER"))
    return encode(hasher.digest())