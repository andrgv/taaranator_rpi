from enum import Enum, auto

class Mode(Enum):
    AIMLESS = auto()
    TRASH_DETECTED = auto()
    BROOMING_AWAY = auto()

class Command(Enum):
    FORWARD = 'F'
    BACK = 'R'
    LEFT = 'L'
    RIGHT = 'R'
    STOP = 'B'
    SENSOR = 'S'