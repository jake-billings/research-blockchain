import os
from encode import encode, decode
from Crypto.PublicKey import RSA
import hashlib

HASHER = hashlib.new('sha224')

KEY_SIZE = 1024
ENTROPY = os.urandom


def key_to_string(key):
    return encode(key.exportKey(format="DER"))


def generate_key():
    return RSA.generate(1024, os.urandom)


def sign(key, data):
    return encode(key.sign(data, '')[0])


def verify(key, signature, data):
    return key.verify(data,(decode(encode(signature), type='long'), None))


def public_key_to_address(key):
    HASHER.update(key.exportKey(format="DER"))
    return encode(HASHER.digest())