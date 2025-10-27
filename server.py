from enums import TransactionState, ValidationType, ServerResponse
class Server: 
    def __init__(self, name: str):
        self.name = name
        self.transactions = {}