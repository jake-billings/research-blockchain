import signature


class Transaction:
    def __init__(self, data, author, signature):
        self.data = data
        self.author = author
        self.signature = signature

    def get_string(self):
        return '%s (%s)' % (self.data, self.author)

    def get_data(self):
        return self.data

    def get_author(self):
        return self.author

    def get_signature(self):
        return self.signature


def sign_transaction(data, key):
    return Transaction(data, signature.sign(key, data), signature.key_to_string(key.publickey()))
