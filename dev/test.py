from faker import Faker
import hashlib
import pprint

from blockchain import Blockchain

pp = pprint.PrettyPrinter(indent=4)
# Create a Faker instance
fake = Faker()

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

bc = Blockchain()

test_create_block(bc)
test_create_transaction(bc)
test_create_block(bc)
test_create_transaction(bc)
test_create_transaction(bc)
test_create_transaction(bc)
test_create_block(bc)
nonce = bc.proof_of_work('dfwfefw33ww', [{'amount':20, 'sender': 'test', 'recipient':'dsfw'}])
print(nonce)
hash = bc.hash_block('dfwfefw33ww', [{'amount':20, 'sender': 'test', 'recipient':'dsfw'}], nonce)
print(hash)