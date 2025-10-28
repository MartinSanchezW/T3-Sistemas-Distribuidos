from enums import TransactionState, ValidationType, ServerResponse

class Transaction:
    def __init__(self, transaction_id: str, start_time: int):
        self.transaction_id = transaction_id
        self.state = None
        self.has_begun = False
        self.read_set = set()
        self.write_set = {}
        self.start_time = start_time
        self.end_time = None #!  Falta setearlo al finalizar

    def begin(self):
        if not self.has_begun:
            self.state = TransactionState.ABIERTA
            self.has_begun = True
            print(f"INFO: {self.transaction_id} -> BEGIN. Estado: {self.state.value}")

    def write(self, key: str, value: str):
        if self.state != TransactionState.ABIERTA:
            if self.state == TransactionState.EN_PREPARACION:
                self.state = TransactionState.INVALIDA
                print(f"ERROR: {self.transaction_id} -> WRITE no permitido en estado {self.state.value}. Debe abortar o esperar commit.")
                return
            print(f"ERROR: {self.transaction_id} -> WRITE no permitido en estado {self.state.value}")
            return
        self.write_set[key] = value
        print(f"INFO: {self.transaction_id} -> WRITE {key}={value}")

    def read(self, key: str, db: dict):
        if self.state != TransactionState.ABIERTA:
            if self.state == TransactionState.EN_PREPARACION:
                self.state = TransactionState.INVALIDA
                print(f"ERROR: {self.transaction_id} -> READ no permitido en estado {self.state.value}. Debe abortar o esperar commit.")
                return 
            print(f"ERROR: {self.transaction_id} -> READ no permitido en estado {self.state.value}")
            return 

        if key in self.write_set:
            value = self.write_set[key]
            self.read_set.add(key)
            print(f"INFO: {self.transaction_id} -> READ {key}={value} (from local)")
            return value
        
        elif key in db:
            value = db[key]
            self.read_set.add(key)
            print(f"INFO: {self.transaction_id} -> READ {key}={value} (from db)")
            return value
        else:
            self.state = TransactionState.INVALIDA
            print(f"ERROR: {self.transaction_id} -> READ {key}= (not found)")

    def abort(self):
        if self.state != TransactionState.CONFIRMADA:
            print(f"INFO: {self.transaction_id} -> ABORT. Estado: {TransactionState.ABORTADA.value}")
            self.state = TransactionState.ABORTADA

    def commit(self):
        pass

        
    def is_finished(self) -> bool:
        return self.state in (
            TransactionState.CONFIRMADA,
            TransactionState.ABORTADA,
            TransactionState.INVALIDA
        )
