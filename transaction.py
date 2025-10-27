from enums import TransactionState, ValidationType, ServerResponse

class Transaction:
    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id
        self.state = None
        self.has_begun = False

    def begin(self):
        pass

    def write(self, key: str, value: str):
        pass

    def read(self, key: str) -> str:
        pass

    def can_commit(self) -> bool:
        pass

    def abort(self):
        pass

    def commit(self):
        pass
