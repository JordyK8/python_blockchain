# from faker import Faker
import hashlib
import pprint

from blockchain import Blockchain

pp = pprint.PrettyPrinter(indent=4)
# Create a Faker instance
# fake = Faker()

def test_create_block(bc):
    # Create a new Blockchain instance
    create_new_block(bc)

def create_new_block(bc):

    # Generate fake data (e.g., a fake string)
    fake_string = fake.text()

    # Create a hash of the fake string
    hash_object = hashlib.sha256(fake_string.encode())
    fake_hash = hash_object.hexdigest()

    # Create another hash of the fake string
    hash_object2 = hashlib.sha256(fake_string.encode())
    fake_hash2 = hash_object2.hexdigest()

    # Generate a fake 4-digit number
    fake_4_digits = fake.numerify(text="####")

    # Create a new block
    bc.create_new_block(fake_4_digits, fake_hash, fake_hash2)

def test_create_transaction(bc):
    # Create random sender, recipient, and amount
    sender = create_random_fake_bank_account()
    recipient = create_random_fake_bank_account()
    amount = fake.random_number()

    bc.create_new_transaction(sender, recipient, amount)

def create_random_fake_bank_account():
    # Generate a random country code (e.g., NL)
    country_code = fake.country_code()

    # Generate a random bank code (e.g., RABO)
    bank_code = ''.join(fake.random_letters(length=4))

    # Generate a random account number (e.g., 789827982)
    account_number = fake.random_number(digits=9)

    # Combine the components to create a bank account-like string
    bank_account_number = f"{country_code}{bank_code}{account_number}"

    return bank_account_number

def check_hash_validation(bc):
    bc1 = {
        "chain": [
            {
                "hash": "0",
                "index": 1,
                "nonce": 100,
                "previous_block_hash": "0",
                "timestamp": 1709234073,
                "transactions": []
            },
            {
                "hash": "00005ad3d62fff3cf1f414ee06c5a7848c3f599475e95f8a81aa1ab1c6a71e11",
                "index": 2,
                "nonce": 54735,
                "previous_block_hash": "0",
                "timestamp": 1709234088,
                "transactions": []
            },
            {
                "hash": "0000a32f8bdc641e035fce0c92fa99ced2424a727baa6bf08a7883f0b0c666aa",
                "index": 3,
                "nonce": 10690,
                "previous_block_hash": "00005ad3d62fff3cf1f414ee06c5a7848c3f599475e95f8a81aa1ab1c6a71e11",
                "timestamp": 1709234167,
                "transactions": [
                    {
                        "amount": 12.5,
                        "recipient": "5a886e27f4834a41b6fa42448b2e2f87",
                        "sender": "00",
                        "transaction_id": "222f4969aa8d44e3bf8a0164ac35bbad"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 10,
                        "transaction_id": "c31dc301759143469d5df1bc6bbe8eb9"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 20,
                        "transaction_id": "764eec79bec14948816301e64d31ecd8"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 30,
                        "transaction_id": "4c069e93517f451a82280642953dab28"
                    }
                ]
            },
            {
                "hash": "0000909cc36cdd6801481f21375eaf4044b6ca39aa2275d2beff621885020e2b",
                "index": 4,
                "nonce": 15341,
                "previous_block_hash": "0000a32f8bdc641e035fce0c92fa99ced2424a727baa6bf08a7883f0b0c666aa",
                "timestamp": 1709234210,
                "transactions": [
                    {
                        "amount": 12.5,
                        "recipient": "5a886e27f4834a41b6fa42448b2e2f87",
                        "sender": "00",
                        "transaction_id": "430fe90b6ebd4b129752ae4cd380bf92"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 40,
                        "transaction_id": "38953bcfb4c84565a8a2f0aeacc596ce"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 50,
                        "transaction_id": "cf8fbd9ebf31480394f187139945f32f"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 60,
                        "transaction_id": "848fcf69fe544eb69ae38e3c69f8e09e"
                    },
                    {
                        "amount": "Jdw23PONY567854765CF",
                        "recipient": "YUGHIUY6785435466VBN",
                        "sender": 70,
                        "transaction_id": "2916838f79064f43b2442632cebf02b6"
                    }
                ]
            },
            {
                "hash": "0000b88e9b1a30c82265789983872e3ec7b9f90d5f1f4ab48f8e055e50345367",
                "index": 5,
                "nonce": 3816,
                "previous_block_hash": "0000909cc36cdd6801481f21375eaf4044b6ca39aa2275d2beff621885020e2b",
                "timestamp": 1709234231,
                "transactions": [
                    {
                        "amount": 12.5,
                        "recipient": "5a886e27f4834a41b6fa42448b2e2f87",
                        "sender": "00",
                        "transaction_id": "bead84422f684c7184ffa83bb9a2c25b"
                    }
                ]
            },
            {
                "hash": "0000dfcffc59b41f974e8ce4bc2d8db30df43df7adc61d0bcfc84dbebe680907",
                "index": 6,
                "nonce": 5821,
                "previous_block_hash": "0000b88e9b1a30c82265789983872e3ec7b9f90d5f1f4ab48f8e055e50345367",
                "timestamp": 1709234232,
                "transactions": [
                    {
                        "amount": 12.5,
                        "recipient": "5a886e27f4834a41b6fa42448b2e2f87",
                        "sender": "00",
                        "transaction_id": "bb5dc2e5e5a948459187fda40501890e"
                    }
                ]
            }
        ],
        "current_node_url": "http://localhost:3001",
        "network_nodes": [],
        "pending_transactions": [
            {
                "amount": 12.5,
                "recipient": "5a886e27f4834a41b6fa42448b2e2f87",
                "sender": "00",
                "transaction_id": "74b06132a48742febe50be3b69670acd"
            }
        ]
    }

    valid = Blockchain.chain_is_valid(bc1["chain"])
    print(valid)

bc = Blockchain()

# test_create_block(bc)
# test_create_transaction(bc)
# test_create_block(bc)
# test_create_transaction(bc)
# test_create_transaction(bc)
# test_create_transaction(bc)
# test_create_block(bc)
# nonce = bc.proof_of_work('dfwfefw33ww', [{'amount':20, 'sender': 'test', 'recipient':'dsfw'}])
# print(nonce)
# hash = bc.hash_block('dfwfefw33ww', [{'amount':20, 'sender': 'test', 'recipient':'dsfw'}], nonce)
# print(hash)
check_hash_validation(bc)