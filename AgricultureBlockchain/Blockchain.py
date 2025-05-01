from hashlib import sha256
import json
import time
import pickle
from datetime import datetime
import random
import pyaes, pbkdf2, binascii, os, secrets
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load encryption key from environment
ENCRYPTION_KEY_HEX = os.environ.get('ENCRYPTION_KEY')
if not ENCRYPTION_KEY_HEX or len(ENCRYPTION_KEY_HEX) != 64: # 32 bytes = 64 hex chars
    raise ValueError("No or invalid ENCRYPTION_KEY set in .env file. Please generate a 32-byte hex key.")
ENCRYPTION_KEY = binascii.unhexlify(ENCRYPTION_KEY_HEX)

# AES block size is 16 bytes
AES_NONCE_BYTES = 16

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    # difficulty of our PoW algorithm
    difficulty = 2 #using difficulty 2 computation

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.peer = []
        self.translist = []

    def create_genesis_block(self): #create genesis block
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof): #adding data to block by computing new and previous hashes
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        # Check if the proof is valid (removed the call to the old is_valid_proof)
        if not proof.startswith('0' * self.difficulty):
             return False
        if proof != block.compute_hash():
             print(f"Proof: {proof}\nComputed: {block.compute_hash()}") # Debugging
             return False

        block.hash = proof
        self.chain.append(block)
        return True

    def proof_of_work(self, block): #proof of work
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
            # Add a check to prevent potential infinite loops in edge cases
            if block.nonce % 1000000 == 0:
                 print(f"PoW nonce approaching {block.nonce}...") # Progress indicator
            if block.nonce > 100000000: # Safety break
                 print("Warning: PoW nonce exceeded limit. Aborting mining.")
                 return None

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def addPeer(self, peer_details):
        self.peer.append(peer_details)

    def addTransaction(self,trans_details): #add transaction
        self.translist.append(trans_details)

    def mine(self):#mine transaction
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        if proof is None: # Handle PoW failure
            print("Mining failed, could not find proof.")
            return False

        added = self.add_block(new_block, proof)
        if not added:
             print("Failed to add block after mining.")
             return False

        self.unconfirmed_transactions = []
        return new_block.index

    def save_object(self,obj, filename):
        try:
            with open(filename, 'wb') as output:
                pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(f"Error saving blockchain state: {e}")

    def encrypt(self, plaintext):
        """Encrypts plaintext using AES-CTR with a random nonce.
        Returns: bytes: nonce + ciphertext
        """
        try:
            # Ensure plaintext is bytes
            if isinstance(plaintext, str):
                plaintext_bytes = plaintext.encode('utf-8')
            else:
                plaintext_bytes = plaintext

            # Generate a random nonce (IV for CTR mode)
            nonce = secrets.token_bytes(AES_NONCE_BYTES)
            aes = pyaes.AESModeOfOperationCTR(ENCRYPTION_KEY, pyaes.Counter(initial_value=int.from_bytes(nonce, 'big')))
            ciphertext = aes.encrypt(plaintext_bytes)
            # Prepend nonce to ciphertext
            return nonce + ciphertext
        except Exception as e:
            print(f"Encryption error: {e}")
            return None # Indicate failure

    def decrypt(self, nonce_ciphertext):
        """Decrypts data encrypted with encrypt method (nonce + ciphertext).
        Args:
            nonce_ciphertext (bytes): The combined nonce and ciphertext.
        Returns: bytes: The original plaintext bytes, or None on error.
        """
        try:
            if len(nonce_ciphertext) < AES_NONCE_BYTES:
                print("Decryption error: Input too short to contain nonce.")
                return None

            # Extract nonce and ciphertext
            nonce = nonce_ciphertext[:AES_NONCE_BYTES]
            ciphertext = nonce_ciphertext[AES_NONCE_BYTES:]

            aes = pyaes.AESModeOfOperationCTR(ENCRYPTION_KEY, pyaes.Counter(initial_value=int.from_bytes(nonce, 'big')))
            decrypted_bytes = aes.decrypt(ciphertext)
            return decrypted_bytes
        except Exception as e:
            print(f"Decryption error: {e}")
            return None # Indicate failure

    
