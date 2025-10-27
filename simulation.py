from enums import TransactionState, ValidationType, ServerResponse
from server import Server
from transaction import Transaction
import json

class Simulation:
    def __init__(self, setup : dict):
        self.db = setup.get("DATA", {})
        self.server_list = setup.get("SERVERS", [])
        self.servers = {name: Server(name) for name in self.server_list}
        self.validation = setup.get("VALIDATION")
        self.events = setup.get("TRANSACTIONS", [])
        self.transactions: dict[str, Transaction] = {}

        self.logs = []


    def read_posible_values(self, key: str):
        possible_values = set()
        if key in self.db:
            possible_values.add(self.db[key])
        for transaction in self.transactions.values():
            if transaction.state == TransactionState.ABIERTA or transaction.state == TransactionState.EN_PREPARACION:
                if key in transaction.write_set:
                    if transaction.write_set[key] != "DELETE":
                        possible_values.add(transaction.write_set[key])

        self.logs.append(json.dumps(list(possible_values)))
    
    def read_commit(self, key:str):
        if key in self.db:
            self.logs.append(self.db[key])
        else:
            self.logs.append("NULL")

    def get_or_create_transaction(self, transaction_id: str) -> Transaction:
        if transaction_id not in self.transactions:
            self.transactions[transaction_id] = Transaction(transaction_id)
        return self.transactions[transaction_id]

    def process_event(self, event: str):
        sections = event.split(";")
        if sections[0] == "C":
            #Consulta 
            action = sections[1]
            key = sections[2]

            if action == "READ_POSSIBLE_VALUES":
                self.read_posible_values(key)
            elif action == "READ_COMMIT":
                self.read_commit(key)

        else:
            transaction = self.get_or_create_transaction(sections[0])
            action = sections[1]
            
            if len(sections) == 2:
                if action == "BEGIN":
                    transaction.begin()
                elif action == "COMMIT":
                    transaction.commit()
                elif action == "ABORT":
                    transaction.abort()

            elif len(sections) == 3:

                key = sections[2]
                if action == "READ":
                    transaction.read(key, self.db)

                elif action == "WRITE":
                    data = key.split(",")
                    transaction.write(data[0], data[1])

    def run(self):
        for event in self.events:
            self.process_event(event)

    