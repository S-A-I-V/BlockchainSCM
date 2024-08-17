from blockchain import Blockchain, Transaction, Block
from participants import Participant
from consensus import ProofOfStake
from dispute_resolution import DisputeResolution
from utils import generate_qr_code_representation

class SupplyChainSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.participants = {}

    def add_participant(self, participant):
        self.participants[participant.id] = participant

    def get_participant(self, participant_id):
        return self.participants.get(participant_id)

def display_menu():
    print("\\nChoose an option:")
    print("1. Register a new participant.")
    print("2. Create a new transaction.")
    print("3. Display blockchain.")
    print("4. Resolve disputes.")
    print("5. Exit.")
    return input("Enter your choice: ")

def main():
    system = SupplyChainSystem()
    resolution = DisputeResolution(system)
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            # Register a new participant
            participant_type = input("Enter participant type (manufacturer, distributor, client): ")
            participant_id = input("Enter participant ID: ")
            deposit = float(input("Enter security deposit (0 for manufacturers): "))
            participant = Participant(participant_id, participant_type, deposit)
            system.add_participant(participant)
            print(f"Participant {participant_id} registered.")

        elif choice == '2':
            # Create a new transaction
            manufacturer_id = input("Enter manufacturer ID: ")
            distributor_id = input("Enter distributor ID: ")
            client_id = input("Enter client ID: ")
            transaction = Transaction(manufacturer_id, distributor_id, client_id)
            transaction.set_timestamp('distributor_got')
            transaction.set_timestamp('distributor_dispatched')
            transaction.set_timestamp('client_received')
            block = Block(system.blockchain.get_last_block().hash, [transaction])
            system.blockchain.add_block(block)
            print("Transaction added to blockchain.")

        elif choice == '3':
            # Display blockchain
            print(system.blockchain)

        elif choice == '4':
            # Resolve disputes
            distributor_claim = input("Distributor's claim (True/False): ") == 'True'
            client_claim = input("Client's claim (True/False): ") == 'True'
            transaction_index = int(input("Enter transaction index (block index in the blockchain): "))
            transaction = system.blockchain.chain[transaction_index].transactions[0]
            result = resolution.resolve(distributor_claim, client_claim, transaction)
            print(result)

        elif choice == '5':
            # Exit the program
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()