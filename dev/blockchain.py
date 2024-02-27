from datetime import datetime
import json
import hashlib
import sys
from uuid import uuid4
port = sys.argv[1]

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        
        self.current_node_url = 'http://localhost:' + port
        self.network_nodes = []

        self.create_new_block(nonce=100, previous_block_hash='0', hash='0')

    def create_new_block(self, nonce, previous_block_hash, hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': int(datetime.utcnow().timestamp()),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'hash': hash,
            'previous_block_hash': previous_block_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)
        # broadcast to all nodes
        return block

    def get_last_block(self):
        return self.chain[-1]
    
    def create_new_transaction(self, sender, recipient, amount):
        return {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'transaction_id': str(uuid4()).replace('-', ''),
        }

    def add_transaction_to_pending_transactions(self, transaction):
        self.pending_transactions.append(transaction)
        return self.get_last_block()['index'] + 1

    def hash_block(self, previous_block_hash, current_block_data, nonce):
        current_block_data_string = json.dumps(current_block_data, sort_keys=True).encode()
        data_as_string = f'{previous_block_hash}{nonce}{current_block_data_string}'
        hash_object = hashlib.sha256(data_as_string.encode())
        return hash_object.hexdigest()

    def proof_of_work(self, previous_block_hash, current_block_data):
        nonce = 0
        hash = self.hash_block(previous_block_hash, current_block_data, nonce)
        while not hash.startswith('0000'):
            nonce += 1
            hash = self.hash_block(previous_block_hash, current_block_data, nonce)
        return nonce

    def __repr__(self):
        indent = ' ' * 4  # Adjust the number of spaces for indentation as needed
        chain_repr = '\n'.join(indent + str(block) for block in self.chain)
        transactions_repr = '\n'.join(indent + str(transaction) for transaction in self.pending_transactions)
        return f'Blockchain(\n{indent}chain=[\n{chain_repr}\n],\n{indent}pending_transactions=[\n{transactions_repr}\n])'