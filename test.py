import blockchain, signature, transaction, nonce_source

from encode import encode
from os import urandom

print 'Mining difficulty: %s:%s' % (blockchain.DIFFICULTY_ORDER, blockchain.DIFFICULTY)


nonce_source = nonce_source.NonceSource('nonce_sources')

key = signature.generate_key()
address = signature.public_key_to_address(key.publickey())

print address

chain = [blockchain.mine_block('', 0, 'genesis', nonce_source, address)]


print chain[0].get_string()

for i in range(1, 100):
    transactions = []

    for j in range(0, i % 3 + 1):
        t = transaction.sign_transaction('random transaction data: %s' % encode(urandom(8)), key)
        transactions.append(t)

    block_data = ''
    for t in transactions:
        block_data += t.get_string()+'\n'

    b = blockchain.mine_block(chain[i-1].get_hash(), i, block_data, nonce_source, address)
    chain.append(b)

    print b.get_string()
