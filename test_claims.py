from encode import encode,decode
import signature

# This is the test data to sign
data = 'test signed data'

# Generate a PyCrypto RSA key using signature module
key = signature.generate_key()

# Sign the test data with the key
sig = signature.sign(key, data)

# Dump encoded versions of the keys and data to the console
print 'private', signature.key_to_string(key)
print 'public', signature.key_to_string(key.publickey())
print 'address', signature.public_key_to_address(key.publickey())
print 'data', data
print 'signature', sig, '\n'

# Test verification code
print 'call to verify() with legit data\t\t\t%s\t(Should be True)' % signature.verify(key, sig, data)
print 'call of verify() with tampered data\t\t\t%s\t(Should be False)' % key.verify(data+'asdf',(decode(encode(sig),type='long'),None))
