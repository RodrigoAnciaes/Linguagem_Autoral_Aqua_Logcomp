import enum

class Tkn(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Tkn({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    
    def __repr__(self):
        return self.__str__()   
    
    class type(enum.Enum):
        BRANCH = 1
        ACUMULATE = 2
        ARROW = 3
        FLOW = 4
        RIVER = 5
        FISH = 6
        DISCOVER = 7
        SUSTAINS = 8
        EVENT = 9
        RAIN = 10
        DRY = 11
        EXTINGUISH = 12
        OPERATION = 13
        PASS_TIME = 14
        CONCLUDE = 15
        CREATE = 16
        COMPARISSON = 17
        NUMBER = 18
        IDENTIFIER = 19
        NEWLINE = 20
        EOF = 21
        PAREN_OPEN = 22
        PAREN_CLOSE = 23
        COMMA = 24

    
    