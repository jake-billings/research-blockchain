import base64

# The encode module abstracts the native base64 library. This provides the freedom to use whatever encoding is desired
# and to change it on the fly. Additionally, code is written to allow for the encoding and decoding of long values.
# This is specifically designed to support encoding of signature from the RSA feature of the PyCrypto library.
# Both base64 and base32 are supported. Base32 is supported specifically for the purpose of spelling out words in
# mining algorithms. It is computationally infeasible to spell out more than two letters in mined blocks in base64;
# however, four and five letter words can be mined with base32 due to the drastically smaller search space.
# Base64 strings are prepended with "0x40_", which is 64 in hex, and base32 strings are prepended with "0x20_", which is
# 32 in hex. This aids debugging of encoded strings.


# Encodes input data as base64 and prepends it with "0x40_". "0x40" is 64 in hex and is used to determines the
# difference between base32 encoded strings and base64 encoded strings in debugging.
# data must be the binary data to be encoded
def encode(data):
    # Pack integers as a byte string
    # https://stackoverflow.com/questions/14764237/how-to-encode-a-long-in-base64-in-python
    if isinstance(data, (int, long)):
        b = bytearray()
        while data:
            b.append(data & 0xFF)
            data >>= 8
        data = b

    return '0x40_'+base64.standard_b64encode(data)


# Decodes input data as base64 and after stripping the "0x40_" prefix. "0x40" is 64 in hex and is used to determines the
# difference between base32 encoded strings and base64 encoded strings in debugging.
def decode(data, type='string'):
    data = base64.standard_b64decode(data[5:])

    # Unpack the long
    # https://stackoverflow.com/questions/14764237/how-to-encode-a-long-in-base64-in-python
    if type is 'long' or type is 'int':
        data = bytearray(data)  # in case you're passing in a bytes/str
        data = sum((1 << (bi * 8)) * bb for (bi, bb) in enumerate(data))

    return data


# Encodes input data as base64 and prepends it with "0x20_". "0x20" is 32 in hex and is used to determines the
# difference between base32 encoded strings and base64 encoded strings in debugging.
def encode_32(data):
    # Pack integers as a byte string
    # https://stackoverflow.com/questions/14764237/how-to-encode-a-long-in-base64-in-python
    if isinstance(data, (int, long)):
        b = bytearray()
        while data:
            b.append(data & 0xFF)
            data >>= 8
        data = b

    return '0x20_'+base64.b32encode(data).lower()


# Decodes input data as base32 and after stripping the "0x20_" prefix. "0x20" is 32 in hex and is used to determines the
# difference between base32 encoded strings and base64 encoded strings in debugging.
def decode_32(data, type='string'):
    data = base64.b32decode(data[5:].upper())

    # Unpack the long
    # https://stackoverflow.com/questions/14764237/how-to-encode-a-long-in-base64-in-python
    if type is 'long' or type is 'int':
        data = bytearray(data)  # in case you're passing in a bytes/str
        data = sum((1 << (bi * 8)) * bb for (bi, bb) in enumerate(data))

    return data
