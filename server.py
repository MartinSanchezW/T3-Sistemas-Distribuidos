from enums import TransactionState, ValidationType, ServerResponse
from transaction import Transaction

class Server: 
    def __init__(self, name: str):
        self.name = name
        self.accepted_transactions = {}

    def can_commit(self, transaction: Transaction, validation_type: ValidationType) -> ServerResponse:
        pass

    def concurrency_control(self, transaction: Transaction, validation_type: ValidationType) -> bool:
        pass

    def tpc_check(self, transaction: Transaction) -> bool:
        pass