
import random

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
