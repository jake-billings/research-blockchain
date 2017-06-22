import signature


class Transaction:
    def __init__(self, data, signature):
        self.data = data
        self.signature = signature

    def get_string(self):
        return '%s (%s)' % (self.data, self.signature)


def sign_transaction(data, key):
    return Transaction(data, signature.sign(key, data))
