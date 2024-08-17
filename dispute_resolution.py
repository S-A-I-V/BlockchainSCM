class DisputeResolution:
    def __init__(self, supply_chain_system):
        self.supply_chain_system = supply_chain_system

    def resolve(self, distributor_claim, client_claim, transaction):
        distributor = self.supply_chain_system.get_participant(transaction.distributor)
        client = self.supply_chain_system.get_participant(transaction.client)
        
        product_dispatched = bool(transaction.timestamps['distributor_dispatched'])
        product_received = bool(transaction.timestamps['client_received'])

        if distributor_claim == product_dispatched and client_claim == product_received:
            return "No dispute."

        if distributor_claim and not client_claim:
            if product_received:
                client.deduct_security(50.0)
                return f"Client {client.id} was found to be dishonest. Deducted 50.0 from security deposit."
            else:
                distributor.deduct_security(50.0)
                return f"Distributor {distributor.id} was found to be dishonest. Deducted 50.0 from security deposit."

        if not distributor_claim and client_claim:
            return "No dispute."