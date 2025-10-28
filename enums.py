from enum import Enum

class TransactionState(Enum):
    ABIERTA = "ABIERTA"                
    EN_PREPARACION = "EN_PREPARACION"  
    CONFIRMADA = "CONFIRMADA"          
    ABORTADA = "ABORTADA"              
    INVALIDA = "INVALIDA"            

class ValidationType(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"

class ServerResponse(Enum):
    VOTE_YES = "VOTE_YES"
    VOTE_NO = "VOTE_NO"
