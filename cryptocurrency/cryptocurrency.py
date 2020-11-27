from hashlib import sha256
from random import randint
import json, time


def Block(index, data, previous_hash):
    nonce = randint(1, 4294967296)
    return {
        'index': index,
        'timestamp': int(time.time()),
        'data': data,
        'previous_hash': previous_hash,
        'hash': sha256((str(data)+str(nonce)).encode()).hexdigest(),
        'nonce': nonce
    }

def Transaction(sender, recipient, amount, b):
    b.pending_transactions.append({
        'from': sender,
        'to': recipient,
        'amount': amount,
    })

def proof_of_work(block):  
    for i in range(1, 4294967296):
        if i == block['nonce']:
            return i
        
class Blockchain:
    def __init__(self):
        self.blockchain = [Block(0, {None: None}, None)]
        self.pending_transactions = []
    def mine(self, miner):
        block = Block(len(self.blockchain), self.pending_transactions[0], self.blockchain[-1]['hash'])
        n = proof_of_work(block)
        self.blockchain.append(block)
        res = round((n/4294967296)*1, 1)
        if res == 0.0:
            return 0.1
        else:
            return res

#b = Blockchain()

#Transaction('luka', 'rahul', 100, b)
#b.mine()

#print(json.dumps(b.blockchain, indent=4))
