from enums import TransactionState, ValidationType, ServerResponse

class Transaction:
    """
    Transacción 2PC
    """
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id
        self.state = None
        self.has_begun = False

        self.read_set = set()
        self.write_set = {}

        self.approved_by_servers = set()

    def begin(self):
        """
        Inicia la transacción si no ha sido iniciada.
        """
        if not self.has_begun:
            self.state = TransactionState.ABIERTA
            self.has_begun = True
            print(f"INFO: {self.transaction_id} -> BEGIN. Estado: {self.state.value}")

    def write(self, key: str, value: str):
        if self.state != TransactionState.ABIERTA:
            if self.state == TransactionState.EN_PREPARACION:
                self.state = TransactionState.INVALIDA
                raise Exception(f"ERROR: {self.transaction_id} -> WRITE no permitido en estado {self.state.value}. Debe abortar o esperar commit.")
            raise Exception(f"ERROR: {self.transaction_id} -> WRITE no permitido en estado {self.state.value}")
        self.write_set[key] = value
        print(f"INFO: {self.transaction_id} -> WRITE {key}={value}")

    def read(self, key: str, db: dict) -> str:
        if self.state != TransactionState.ABIERTA:
            if self.state == TransactionState.EN_PREPARACION:
                self.state = TransactionState.INVALIDA
                raise Exception(f"ERROR: {self.transaction_id} -> READ no permitido en estado {self.state.value}. Debe abortar o esperar commit.")
            raise Exception(f"ERROR: {self.transaction_id} -> READ no permitido en estado {self.state.value}")
        
        if key in self.write_set:
            value = self.write_set[key]
            print(f"INFO: {self.transaction_id} -> READ {key}={value} (from write set)")
            return value
        
        elif key in db:
            value = db[key]
            self.read_set.add(key)
            print(f"INFO: {self.transaction_id} -> READ {key}={value} (from db)")
            return value
        else:
            self.state = TransactionState.INVALIDA
            raise Exception(f"ERROR: {self.transaction_id} -> READ {key}= (not found)")

    def can_commit(self) -> bool:
        pass

    def abort(self):
        pass

    def commit(self):
        pass
