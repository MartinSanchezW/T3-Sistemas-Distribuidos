from enum import Enum

class TransactionState(Enum):
    """
    Define los posibles estados de una transacción.
    """
    ABIERTA = "ABIERTA"                
    EN_PREPARACION = "EN_PREPARACION"  
    CONFIRMADA = "CONFIRMADA"          
    ABORTADA = "ABORTADA"              
    INVALIDA = "INVALIDA"            

class ValidationType(Enum):
    """
    Define los tipos de validación de concurrencia.
    """
    FORWARD = "forward"
    BACKWARD = "backward"

class ServerResponse(Enum):
    """
    Posibles respuestas de un servidor a un CAN_COMMIT.
    """
    ACCEPT = "ACCEPT"
    REJECT_2PC = "REJECT_2PC"
    REJECT_CC_FORWARD = "REJECT_CC_FORWARD"
    REJECT_CC_BACKWARD = "REJECT_CC_BACKWARD"