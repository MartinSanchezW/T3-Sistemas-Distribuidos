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
        self.time = 0
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
            self.transactions[transaction_id] = Transaction(transaction_id, self.time)
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
                elif action == "ABORT":
                    transaction.abort()
                elif action == "COMMIT":
                    self.commit(transaction)

            elif len(sections) == 3:

                key = sections[2]
                if action == "READ":
                    transaction.read(key, self.db)

                elif action == "WRITE":
                    data = key.split(",")
                    transaction.write(data[0], data[1])

                elif action == "CAN_COMMIT":
                    self.can_commit(sections[2], transaction)
            self.time += 1

    def run(self):
        for event in self.events:
            self.process_event(event)

    def generate_output_file(self):
        with open("simulation_log.txt", "w", encoding="utf-8") as f:
            f.write("##LOGS##\n")
            if len(self.logs) == 0:
                f.write("No hubo logs\n")
            for log in self.logs:
                f.write(log + "\n")

            f.write("##DATABASE##\n")
            for key, value in self.db.items():
                f.write(f"{key}={value}\n")

            f.write("##STATS##\n")
            stats = self.get_stats()
            f.write(f"ABIERTA={json.dumps(list(stats['ABIERTA']))}\n")
            f.write(f"ABORTADA={json.dumps(list(stats['ABORTADA']))}\n")
            f.write(f"CONFIRMADA={json.dumps(list(stats['CONFIRMADA']))}\n")
            f.write(f"EN_PREPARACION={json.dumps(list(stats['EN_PREPARACION']))}\n")
            f.write(f"INVALIDA={json.dumps(list(stats['INVALIDA']))}\n")

    def get_stats(self) -> dict:
        stats = {"ABIERTA": [], "ABORTADA": [], "INVALIDA": [], "CONFIRMADA": [], "EN_PREPARACION": []}
        for transaction in self.transactions.values():
            stats[transaction.state.value].append(transaction.transaction_id)
        return stats
    
    def can_commit(self, server_name: str, transaction: Transaction) -> None:
        # find server with server name in self.servers
        validation_type = ValidationType.FORWARD if self.validation == "forward" else ValidationType.BACKWARD
        server = self.servers[server_name]
        server.prepare(transaction, self.transactions, validation_type)
        # Se actualiza el servidor internamente.
    
    def commit(self, transaction: Transaction) -> None:
        isQuorumOk = len(transaction.approved_by_servers) >= (len(self.server_list) // 2) + 1

        isStateValid = transaction.state == TransactionState.EN_PREPARACION

        isBackwardValid = self.backward_control(transaction)

        if isQuorumOk and isStateValid and isBackwardValid:
            # Commit
            # 1) Se distribuye a todos los servidores el commit
            for server in self.servers.values():
                server.accept_transaction(transaction)

            # 2) Se aplican los cambios a la base de datos
            for key, value in transaction.write_set.items():
                if value == "DELETE":
                    if key in self.db:
                        del self.db[key]
                else:
                    self.db[key] = value
            transaction.state = TransactionState.CONFIRMADA
            transaction.end_time = self.time
            print(f"INFO: {transaction.transaction_id} -> COMMIT. Estado: {transaction.state.value}")

            # 3) Se liberan los recursos bloqueados en cada servidor
            # ! REVISAR EL MANEJO DE LOCKED RESOURCES
            for server in self.servers.values():
                for key in transaction.write_set.keys():
                    if key in server.locked_resources:
                        server.locked_resources.remove(key)

            # 4) Abortar transacciones que leen datos escritos por esta
            for server in self.servers.values():
                for other_transaction in server.accepted_transactions.values():
                    if other_transaction.transaction_id == transaction.transaction_id:
                        continue
                    if other_transaction.state == TransactionState.ABIERTA or other_transaction.state == TransactionState.EN_PREPARACION:
                        for key in transaction.write_set.keys():
                            if key in other_transaction.read_set:
                                other_transaction.abort()
                                print(f"INFO: {other_transaction.transaction_id} -> ABORT (due to commit of {transaction.transaction_id}). Estado: {other_transaction.state.value}")


    def backward_control(self, transaction: Transaction) -> bool:
        read_set = transaction.read_set
        for key in read_set:
            for other_transaction in self.transactions.values():
                if other_transaction.transaction_id == transaction.transaction_id:
                    continue
                if (other_transaction.state == TransactionState.CONFIRMADA) and (
                    other_transaction.end_time > transaction.start_time
                ):
                    if key in other_transaction.write_set:
                        transaction.abort()
                        return False
        return True
        


