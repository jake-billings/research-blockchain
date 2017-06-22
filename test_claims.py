import os
from encode import encode,decode
import Crypto.PublicKey.RSA as RSA

data = 'test signed data'


def key_to_string(key):
    return encode(key.exportKey(format="DER"))

key = RSA.generate(1024, os.urandom)

signature = key.sign(data, '')[0]

print 'private', key_to_string(key)
print 'public', key_to_string(key.publickey())
print 'data', data
print 'signature', encode(signature)

print 'verification', key.verify(data,(decode(encode(signature),type='long'),None))
print 'tampering', key.verify(data+'asdf',(decode(encode(signature),type='long'),None))
