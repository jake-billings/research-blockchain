import base64


# https://stackoverflow.com/questions/14764237/how-to-encode-a-long-in-base64-in-python
def encode(data):
    # Pack integers as a byte stirng
    if isinstance(data, (int, long)):
        b = bytearray()
        while data:
            b.append(data & 0xFF)
            data >>= 8
        data = b

    return '0x40_'+base64.standard_b64encode(data)


def decode(data, type='string'):
    data = base64.standard_b64decode(data[5:])

    # Unpack the long
    if type is 'long' or type is 'int':
        data = bytearray(data)  # in case you're passing in a bytes/str
        data = sum((1 << (bi * 8)) * bb for (bi, bb) in enumerate(data))

    return data


def encode_32(data):
    # Pack integers as a byte stirng
    if isinstance(data, (int, long)):
        b = bytearray()
        while data:
            b.append(data & 0xFF)
            data >>= 8
        data = b

    return '0x20_'+base64.b32encode(data).lower()


def decode_32(data, type='string'):
    data = base64.b32decode(data[5:].upper())

    # Unpack the long
    if type is 'long' or type is 'int':
        data = bytearray(data)  # in case you're passing in a bytes/str
        data = sum((1 << (bi * 8)) * bb for (bi, bb) in enumerate(data))

    return data
