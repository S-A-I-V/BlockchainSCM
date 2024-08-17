
import hashlib
import time
import random

class Transaction:
    def __init__(self, manufacturer, distributor, client, amount=None):
        self.manufacturer = manufacturer
        self.distributor = distributor
        self.client = client
        self.amount = amount
        self.timestamps = {
            'distributor_got': None,
            'distributor_dispatched': None,
            'client_received': None
        }

    def set_timestamp(self, event):
        self.timestamps[event] = time.time()

    def __repr__(self):
        return f"Transaction(manufacturer={self.manufacturer}, distributor={self.distributor}, client={self.client}, amount={self.amount}, timestamps={self.timestamps})"

class Block:
    def __init__(self, prev_hash, transactions):
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()
        self.validator_id = None

    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.merkle_root}{self.prev_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def calculate_merkle_root(self):
        transaction_hashes = [hashlib.sha256(str(t).encode()).hexdigest() for t in self.transactions]
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            transaction_hashes = [hashlib.sha256((transaction_hashes[i] + transaction_hashes[i+1]).encode()).hexdigest() for i in range(0, len(transaction_hashes), 2)]
        return transaction_hashes[0] if transaction_hashes else ""

    def __repr__(self):
        return f"Block(timestamp={self.timestamp}, merkle_root={self.merkle_root}, prev_hash={self.prev_hash}, hash={self.hash})"

class Participant:
    def __init__(self, identifier, role, security_deposit=0.0):
        self.id = identifier
        self.role = role
        self.security_deposit = security_deposit
        self.active_transaction = None

    def deposit_security(self, amount):
        self.security_deposit += amount

    def deduct_security(self, amount):
        self.security_deposit -= amount
        if self.security_deposit < 0:
            self.security_deposit = 0

    def __repr__(self):
        return f"Participant(id={self.id}, role={self.role}, security_deposit={self.security_deposit}, active_transaction={self.active_transaction})"

class ProofOfStake:
    def __init__(self, supply_chain_system):
        self.supply_chain_system = supply_chain_system

    def select_validator(self):
        participants = [p for p in self.supply_chain_system.participants.values() if p.role in ['distributor', 'client']]
        total_staked = sum([p.security_deposit for p in participants])
        select_point = random.uniform(0, total_staked)
        
        current_sum = 0
        for participant in participants:
            current_sum += participant.security_deposit
            if current_sum >= select_point:
                return participant

    def validate(self, block):
        validator = self.supply_chain_system.get_participant(block.validator_id)
        return validator and validator.security_deposit > 0

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.participants = {}
        self.pos = ProofOfStake(self)

    def create_genesis_block(self):
        return Block("0", [])

    def add_participant(self, participant):
        self.participants[participant.id] = participant

    def get_participant(self, participant_id):
        return self.participants.get(participant_id, None)

    def add_block(self, block):
        validator = self.pos.select_validator()
        if validator is None:
            return False
        block.validator_id = validator.id
        
        if self.pos.validate(block):
            self.chain.append(block)
            return True
        return False

    def get_last_block(self):
        return self.chain[-1]

    def __repr__(self):
        return f"Blockchain(chain={self.chain}, pending_transactions={self.pending_transactions})"
