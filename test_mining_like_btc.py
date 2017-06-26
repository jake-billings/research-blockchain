import blockchain_like_btc as blockchain

# Print welcome message
print 'Mining at difficulty order %s, which corresponds to a difficulty of %s hashes' % (blockchain.DIFFICULTY_ORDER, blockchain.DIFFICULTY)

# Mine and print the genesis block, which has no previous block and no information
chain = [blockchain.mine_block(None, 'genesis')]
print chain[0].get_string()

# Mine 10 blocks to demonstrate the working blockchain
for i in range(1, 10):
    b = blockchain.mine_block(chain[i-1], 'block'+str(i))
    chain.append(b)
    print b.get_string()
