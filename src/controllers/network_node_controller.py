from flask import jsonify, request, Blueprint
from uuid import uuid4
import asyncio
import aiohttp
from src.utils.blockchain import Blockchain

bc = Blockchain()

# user controller blueprint to be registered with api blueprint
enx_blockchain = Blueprint("enx_blockchain", __name__)

# Generate a globally unique address for this node
node_address = str(uuid4()).replace('-', '')

# Route to test server
@enx_blockchain.route('/', methods=['GET'])
def test_server():
    return jsonify({'message': 'Server is running!'})

# Route to get all blocks
@enx_blockchain.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({
        'chain': bc.chain,
        'pending_transactions': bc.pending_transactions,
        'network_nodes': bc.network_nodes,
        'current_node_url': bc.current_node_url,
    })

# Route to create a new transaction
@enx_blockchain.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.json
    transaction = data['new_transaction']
    block_index = bc.add_transaction_to_pending_transactions(transaction)
    return jsonify({
        'message': f'Transaction will be added to Block {block_index}',
    })

# Mine a new block
@enx_blockchain.route('/mine', methods=['PUT'])
async def mine_block():
    last_block = bc.get_last_block()
    previous_block_hash = last_block['hash']

    current_block_data = {
        'transactions': bc.pending_transactions,
        'index': last_block['index'] + 1,
    }

    nonce = bc.proof_of_work(previous_block_hash, current_block_data)

    block_hash = bc.hash_block(previous_block_hash, current_block_data, nonce)
 
    block = bc.create_new_block(nonce, previous_block_hash, block_hash)

    # Broadcast the new block to the network
    async def broadcast_block(node, block):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node}/receive-new-block', json={'block': block}) as response:
                return response.text()

     # Handle tasks concurrently
    tasks = [broadcast_block(node, block) for node in bc.network_nodes]
    await asyncio.gather(*tasks)
    # broadcast reward transaction
    async def broadcast_reward_transaction(node):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node}/transaction/broadcast', json={'sender': '00', 'recipient': node_address,'amount': 12.5}) as response:
                return response.text()

     # Handle broadcasting transaction
    await broadcast_reward_transaction(bc.current_node_url)

    return jsonify({
        'message': 'New block mined successfully and broadcast across the network nodes',
        'block': block,
    })

# Receive new block
@enx_blockchain.route("/receive-new-block", methods=["POST"])
def add_block_to_chain():
    data = request.json
    block = data['block']

    # Verify block
    last_block = bc.get_last_block()
    print('last_block', last_block)
    if last_block['hash'] != block['previous_block_hash'] or last_block['index'] + 1 != block['index']:
        return jsonify({
            'message': 'Block received not good',
            'refused_block': block
        })
    
    # add_block
    bc.chain.append(block)

    # empty pending_transactions
    bc.pending_transactions = []

    return jsonify({
        'message': 'New block accepted and processed',
        'new_block': block   
    })

# Register a new node and broadcast it to the network
@enx_blockchain.route('/register-and-broadcast-node', methods=['POST'])
async def register_and_broadcast_node():
    data = request.json
    new_node_url = data['new_node_url']

    # Register the new node only if it is not already in the list
    if not new_node_url in bc.network_nodes:
        bc.network_nodes.append(new_node_url)
    
    # Broadcast the new node to the network
    async def register_node(node, new_node_url):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node}/register-node', json={'new_node_url': new_node_url}) as response:
                return await response.text()
            
    # Handle tasks concurrently
    tasks = [register_node(node, new_node_url) for node in bc.network_nodes]
    data = await asyncio.gather(*tasks)

    # Register the existing nodes on the new node
    async def bulk_register_data(all_network_nodes, new_node_url):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{new_node_url}/register-nodes-bulk', json={'all_network_nodes': all_network_nodes}) as response:
                return await response.text()
   
    # Handle task
    all_network_nodes = bc.network_nodes + [bc.current_node_url]
    bulk_register_data = await bulk_register_data(all_network_nodes, new_node_url)
    print(bulk_register_data)
    
    return jsonify({
        'message': 'New node registered successfully',
    })


# Register a new node
@enx_blockchain.route('/register-node', methods=['POST'])
def register_node():
    data = request.json
    new_node_url = data['new_node_url']

    # Register the new node only if it is not already in the list and it is not the current node
    if not new_node_url in bc.network_nodes and bc.current_node_url != new_node_url:
        bc.network_nodes.append(new_node_url)
        return jsonify({
            'message': 'New node registered successfully',
        })
    
    return jsonify({
        'message': 'Node already registered',
    })

# Register nodes in bulk
@enx_blockchain.route('/register-nodes-bulk', methods=['POST'])
def register_nodes_bulk():
    data = request.json
    all_network_nodes = data['all_network_nodes']
    
    for node in all_network_nodes:
        if not node in bc.network_nodes and node != bc.current_node_url:
            bc.network_nodes.append(node)

    return jsonify({
        'message': 'Bulk registration successful',
    })

# Broadcast a transaction to the network    
@enx_blockchain.route('/transaction/broadcast', methods=['POST'])
async def broadcast_transaction():
    data = request.json
    sender, recipient, amount = data.values()

    new_transaction = bc.create_new_transaction(sender, recipient, amount)
    bc.add_transaction_to_pending_transactions(new_transaction)

    # Broadcast the new transaction to the network
    async def bulk_broadcast_transaction(node_url, new_transaction):
        print(new_transaction, node_url)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node_url}/transaction', json={'new_transaction': new_transaction}) as response:
                return await response.text()
  
    # Handle tasks concurrently
    tasks = [bulk_broadcast_transaction(node, new_transaction) for node in bc.network_nodes]
    data = await asyncio.gather(*tasks)
    return jsonify({
        'message':'Succesfully created and broadcast transaction'
    })

# # Consensus
@enx_blockchain.route('/consensus', methods=['GET'])
async def consensus():
    # Get chain request
    async def get_chain(node):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{node}/blockchain') as response:
                return await response.json()
    
    # handle tasks concurrently
    tasks = [get_chain(node) for node in bc.network_nodes]
    blockchains = await asyncio.gather(*tasks)
    if not len(blockchains):
        return jsonify({
            'message': "It seems like your the only one on the network, make sure your registered in the network before asking for consensus"
        })
    print(blockchains)

    return_message = 'Current chain not replaced'

    # Find longest chain
    longest_chain_in_network = max(blockchains, key=lambda x: len(x['chain']))
    print(longest_chain_in_network)
    print(bc.chain)
    print(longest_chain_in_network['chain'])
    if len(longest_chain_in_network['chain']) > len(bc.chain):
        # Replace current pending transactions with longest chain trasactions when longest chain valid
        if Blockchain.chain_is_valid(longest_chain_in_network['chain']):
            bc.pending_transactions = longest_chain_in_network['pending_transactions']
            bc.chain = longest_chain_in_network['chain']
            return_message = 'Chain has been replaced'
        else:
            return_message = "Longerchain is not valid, current chain not replaced"
    return jsonify({
        'message': return_message,
        'chain': bc.chain
    })

#video @6:50:00