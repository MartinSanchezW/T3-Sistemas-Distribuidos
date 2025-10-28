from enums import TransactionState, ValidationType, ServerResponse
from transaction import Transaction

class Server: 
    def __init__(self, name: str):
        self.name = name
        self.accepted_transactions = {}
        self.locked_resources = set()

    def accept_transaction(self, transaction: Transaction):
        self.accepted_transactions[transaction.transaction_id] = transaction

    def prepare(self, transaction: Transaction, 
                   allTransactions: dict[str, Transaction],
                   validation_type: ValidationType,
                    ) -> None:
        
        if transaction.transaction_id in self.accepted_transactions:
            return 

        if validation_type == ValidationType.FORWARD:
            write_set = transaction.write_set
            for key in write_set.keys():
                for other_transaction in allTransactions.values():
                    if other_transaction.transaction_id == transaction.transaction_id:
                        continue
                    if (other_transaction.state == TransactionState.ABIERTA
                        ) or (other_transaction.state == TransactionState.EN_PREPARACION):

                        if key in other_transaction.read_set:
                            return 
        else: 
            read_set = transaction.read_set
            for key in read_set:
                for other_transaction in allTransactions.values():
                    if other_transaction.transaction_id == transaction.transaction_id:
                        continue
                    if (other_transaction.state == TransactionState.CONFIRMADA) and (
                        other_transaction.end_time > transaction.start_time
                    ):
                        if key in other_transaction.write_set:
                            transaction.abort()
                            return 
                        
        # Validación de 2PC
        for key in transaction.write_set.keys():
            print("key to lock:", key, "locked resources:", self.locked_resources)
            if key in self.locked_resources:
                return
        
        for key in transaction.read_set:
            if key in self.locked_resources:
                return
        
        # Si no rechazó antes de esto, entonces bloqueamos recursos
        for key in transaction.write_set.keys():
            self.locked_resources.add(key)
        
        transaction.state = TransactionState.EN_PREPARACION # Actualizamos
        
        self.accepted_transactions[transaction.transaction_id] = transaction

        return




