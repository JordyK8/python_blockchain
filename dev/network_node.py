from flask import Flask, jsonify, request
import json
from uuid import uuid4
import asyncio
import aiohttp

from blockchain import Blockchain, port


app = Flask(__name__)
bc = Blockchain()
node_address = str(uuid4()).replace('-', '')

# Route to test server
@app.route('/', methods=['GET'])
def test_server():
    return jsonify({'message': 'Server is running!'})

# Route to get all blocks
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    return jsonify({
        'chain': bc.chain,
        'pending_transactions': bc.pending_transactions,
        'network_nodes': bc.network_nodes,
        'current_node_url': bc.current_node_url,
    })

# Route to create a new transaction
@app.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.json
    transaction = data['new_transaction']
    block_index = bc.add_transaction_to_pending_transactions(transaction)
    return jsonify({
        'message': f'Transaction will be added to Block {block_index}',
    })

# Mine a new block
@app.route('/mine', methods=['PUT'])
async def mine_block():
    last_block = bc.get_last_block()
    previous_block_hash = last_block['hash']

    current_block_data = {
        'transactions': bc.pending_transactions,
        'index': last_block['index'] + 1,
    }
    nonce = bc.proof_of_work(previous_block_hash, current_block_data)

    block_hash = bc.hash_block(previous_block_hash, current_block_data, nonce)

    bc.create_new_transaction('00', node_address, 12.5)
 
    block = bc.create_new_block(nonce, previous_block_hash, block_hash)

    async def broadcast_block(node, block):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node}/receive-new-block', json={'block': block}) as response:
                return response.text()

    tasks = [broadcast_block(node, block) for node in bc.network_nodes]
    await asyncio.gather(*tasks)

    return jsonify({
        'message': 'New block mined successfully and broadcast across the network nodes',
        'block': block,
    })

# Receive new block
@app.route("/receive-new-block", methods=["POST"])
def add_block_to_chain():
    data = request.json
    block = data['block']

    # verify block
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
@app.route('/register-and-broadcast-node', methods=['POST'])
async def register_and_broadcast_node():
    data = request.json
    new_node_url = data['new_node_url']
    if not new_node_url in bc.network_nodes:
        bc.network_nodes.append(new_node_url)
    
    async def register_node(node, new_node_url):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node}/register-node', json={'new_node_url': new_node_url}) as response:
                return await response.text()
    print('nodes:', bc.network_nodes)
    tasks = [register_node(node, new_node_url) for node in bc.network_nodes]
    data = await asyncio.gather(*tasks)

    async def bulk_register_data(all_network_nodes, new_node_url):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{new_node_url}/register-nodes-bulk', json={'all_network_nodes': all_network_nodes}) as response:
                return await response.text()
  
    all_network_nodes = bc.network_nodes + [bc.current_node_url]
    bulk_register_data = await bulk_register_data(all_network_nodes, new_node_url)
    print(bulk_register_data)
    
    return jsonify({
        'message': 'New node registered successfully',
    })


# Register a new node
@app.route('/register-node', methods=['POST'])
def register_node():
    data = request.json
    new_node_url = data['new_node_url']
    if not new_node_url in bc.network_nodes and bc.current_node_url != new_node_url:
        bc.network_nodes.append(new_node_url)
        return jsonify({
            'message': 'New node registered successfully',
        })
    print('nodes:', bc.network_nodes)
    return jsonify({
        'message': 'Node already registered',
    })

# Register nodes in bulk
@app.route('/register-nodes-bulk', methods=['POST'])
def register_nodes_bulk():
    data = request.json
    print('data:', data)
    all_network_nodes = data['all_network_nodes']
    print('all_network_nodes:', all_network_nodes)
    for node in all_network_nodes:
        if not node in bc.network_nodes and node != bc.current_node_url:
            bc.network_nodes.append(node)
    print('nodes:', bc.network_nodes)
    return jsonify({
        'message': 'Bulk registration successful',
    })

# Broadcast a transaction to the network    
@app.route('/transaction/broadcast', methods=['POST'])
async def broadcast_transaction():
    data = request.json
    sender, recipient, amount = data.values()
    print(sender, recipient, amount)
    print(data)
    new_transaction = bc.create_new_transaction(sender, recipient, amount)
    bc.add_transaction_to_pending_transactions(new_transaction)

    async def bulk_broadcast_transaction(node_url, new_transaction):
        print(new_transaction, node_url)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{node_url}/transaction', json={'new_transaction': new_transaction}) as response:
                return await response.text()
  
    
    tasks = [bulk_broadcast_transaction(node, new_transaction) for node in bc.network_nodes]
    data = await asyncio.gather(*tasks)
    return jsonify({
        'message':'Succesfully created and broadcast transaction'
    })


if __name__ == '__main__':
    app.run(debug=True, port=port)


#video @5:31:21