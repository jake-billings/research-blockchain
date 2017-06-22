import blockchain

chain = [blockchain.mine_block(None, 'genesis')]
for i in range(1,1000):
    b = blockchain.mine_block(chain[i-1], 'block'+str(i))
    chain.append(b)
    print b.get_string()
