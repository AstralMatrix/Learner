from enum import Enum


class FormReturnStatus(Enum):
    STOP   : int = -1
    RUNNING: int =  0
    RESTART: int =  1
