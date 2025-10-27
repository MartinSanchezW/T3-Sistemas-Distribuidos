from enums import TransactionState, ValidationType, ServerResponse
from server import Server
from transaction import Transaction

class Simulation:
    def __init__(self, setup : dict):
        self.db = setup.get("DATA", {})
        self.server_list = setup.get("SERVERS", [])
        self.servers = [Server(name) for name in self.server_list]
        self.validation = setup.get("VALIDATION")
        self.transaction_list = setup.get("TRANSACTIONS", [])
        self.transactions: list[Transaction] = []


    def read_posible_values(self, key: str) -> set:
        possible_values = set()
        if key in self.db:
            possible_values.add(self.db[key])
        for server in self.servers:
            for transaction in server.transactions.values():
                if key in transaction.write_set:
                    possible_values.add(transaction.write_set[key])
        return possible_values

    