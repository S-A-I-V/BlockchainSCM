
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
