from datetime import datetime
import json
import hashlib
from uuid import uuid4
from src.config.config import Config
config = Config().dev_config

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        
        self.current_node_url = 'http://localhost:' + str(config.PORT)
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

    @staticmethod
    def hash_block(previous_block_hash, current_block_data, nonce):
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
    
    @staticmethod
    def chain_is_valid(chain):
        valid_chain = True
        chain_length = len(chain)
        if chain_length > 1:
            for index in range(1, chain_length):
                print('index',index)
                print('chain',chain)
                block = chain[index]
                previous_block = chain[index - 1]
                 
                 # Hash block to validate hash
                block_hash = Blockchain.hash_block(
                    previous_block['hash'],  
                    {
                        'transactions': block['transactions'],
                        'index': block['index'],
                    },  
                    block["nonce"]  
                )

                # Check validity per block
                if not block_hash.startswith('0000') or block['previous_block_hash'] != previous_block['hash']:
                    valid_chain = False
                    break
        else:
            valid_chain = False  # Chain with less than 2 blocks is considered invalid
        
        # Check genisis block
        genesis_block = chain[0]
        correct_nonce = genesis_block['nonce'] == 100
        correct_block = genesis_block['previous_block_hash'] == '0' 
        correct_hash = genesis_block['hash'] == '0' 
        correct_index = genesis_block['index'] == 1
        correct_transactions = len(genesis_block['transactions']) == 0
        if not correct_nonce or not correct_block or not correct_hash or not correct_transactions or not correct_index:
            valid_chain = False
        
        # return result
        return valid_chain



    def __repr__(self):
        indent = ' ' * 4  # Adjust the number of spaces for indentation as needed
        chain_repr = '\n'.join(indent + str(block) for block in self.chain)
        transactions_repr = '\n'.join(indent + str(transaction) for transaction in self.pending_transactions)
        return f'Blockchain(\n{indent}chain=[\n{chain_repr}\n],\n{indent}pending_transactions=[\n{transactions_repr}\n])'