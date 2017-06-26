import signature


# The Transaction class contains a piece of data, an author address, and a signature.
# This represents a claim made on the block chain. Transactions will be added to blocks.
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


# Sign a piece of data as a transaction using a given PyCrypto key
#
# data must be a string claim to be made on the blockchain
# key must be a PyCrypto RSA key
def sign_transaction(data, key):
    return Transaction(data, signature.sign(key, data), signature.public_key_to_address(key.publickey()))
