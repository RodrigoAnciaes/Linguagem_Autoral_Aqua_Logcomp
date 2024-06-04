
from tknizer import Tknizer
from tkn import Tkn
from node import *
from symbolTable import Symbol_Table

'''
## EBNF

``` 
BLOCK = { STATEMENT };
STATEMENT = ( "λ" | SPAWN | DISCOVER | SUSTAIN | EVENT | RAIN | DRY | EXTINCTION | OPERATION ), "\n" ;
SPAWN = TYPE, IDENTIFIER, "create", ( "λ" | NUMBER | NUMBER, ",", NUMBER ) ;
DISCOVER = "discover", "(", IDENTIFIER, ")" ;
SUSTAIN = IDENTIFIER, "sustains", IDENTIFIER, "\n", "λ", { ( STATEMENT ), "λ" }, "pass_time" ;
EVENT = "event", IDENTIFIER, COMPARISSON, IDENTIFIER, "\n", "λ", { ( STATEMENT ), "λ" }, "conclude" ;
RAIN = "rain","(", IDENTIFIER, ")" ;
DRY = "dry","(", IDENTIFIER, ")" ;
EXTINCTION = "extinguish", IDENTIFIER ; 
OPERATION = IDENTIFIER, OP_T, NUMBER, ( "λ" | OP_T, IDENTIFIER ) ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( "a" | "..." | "z" | "A" | "..." | "Z" ) ;
DIGIT = ( "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" );
TYPE = ( "river" | "fish" ) ;
OP_T = ( "branch" | "acumulate" | ">>" | "->" ) ;

```

Um exemplo limpo de código em Aqua é:

```
river x create 10
river y create 10
x >> 5 >> y
discover(x)
discover(y)
x branch 5
discover(x)
y >> 1 >> x
x acumulate 5
fish z create 2,1
fish f create 1,1
x sustains z:
y >> 1 >> x:
f -> z   
event z inf f 
extingish f
conclude
pass_time
rain(y)
dry(x)

```
'''




class Prsr(object):

    @staticmethod   
    def parse_statement(tknizer, symbol_table):
        #print("teste: ",tknizer.next.type)
        if tknizer.next.type == Tkn.type.EOF or tknizer.next.type == Tkn.type.NEWLINE:
            tknizer.select_next()
            return NoOp()
        if tknizer.next.type == Tkn.type.FISH or tknizer.next.type == Tkn.type.RIVER:
            result =  Prsr.parse_spawn(tknizer, symbol_table)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
        if tknizer.next.type == Tkn.type.DISCOVER:
            result = Prsr.parse_discover(tknizer, symbol_table)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
        if tknizer.next.type == Tkn.type.EVENT:
            result = Prsr.parse_event(tknizer, symbol_table)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
        if tknizer.next.type == Tkn.type.RAIN:
            result = Prsr.parse_rain(tknizer, symbol_table)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
        if tknizer.next.type == Tkn.type.DRY:
            result = Prsr.parse_dry(tknizer, symbol_table)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
        if tknizer.next.type == Tkn.type.EXTINGUISH:
            result = Prsr.parse_extinguish(tknizer, symbol_table)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
        if tknizer.next.type == Tkn.type.IDENTIFIER:
            name = tknizer.next.value
            name = Identifier(name, symbol_table)
            tknizer.select_next()
            if tknizer.next.type == Tkn.type.SUSTAINS:
                result = Prsr.parse_sustains(tknizer, symbol_table, name)
            else:
                result = Prsr.parse_operation(tknizer, symbol_table, name)
            if (tknizer.next.type != Tkn.type.NEWLINE) and (tknizer.next.type != Tkn.type.EOF):
                raise Exception('Expected newline')
            return result
    
    

    @staticmethod
    def parse_spawn(tknizer, symbol_table):
        type = ''
        if tknizer.next.type == Tkn.type.FISH:
            type = 'fish'
        else:
            type = 'river'
        tknizer.select_next()
        name = tknizer.next.value
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.CREATE:
            raise Exception('Expected create')
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.NUMBER:
            raise Exception('Expected number')
        value = int(tknizer.next.value)
        tknizer.select_next()
        if tknizer.next.type == Tkn.type.COMMA:
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.NUMBER:
                raise Exception('Expected number')
            value2 = int(tknizer.next.value)
            tknizer.select_next()
        else:
            value2 = 0
            #tknizer.select_next()
        return Create(name, value, value2, symbol_table, type)
    
    @staticmethod
    def parse_discover(tknizer, symbol_table):
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.PAREN_OPEN:
            raise Exception('Expected (')
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.PAREN_CLOSE:
            raise Exception('Expected )')
        tknizer.select_next()
        return Discover(name)
    
    @staticmethod
    def parse_sustains(tknizer, symbol_table, name):
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name2 = tknizer.next.value
        name2 = Identifier(name2, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.NEWLINE:
            raise Exception('Expected newline')
        tknizer.select_next()
        result = []
        while tknizer.next.type != Tkn.type.PASS_TIME and tknizer.next.type != Tkn.type.EOF:
            result.append(Prsr.parse_statement(tknizer, symbol_table))
        if tknizer.next.type != Tkn.type.PASS_TIME:
            raise Exception('Expected pass_time')
        tknizer.select_next()
        return Sustains(result, name, name2, symbol_table)

    @staticmethod
    def parse_event(tknizer, symbol_table):
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.COMPARISSON:
            raise Exception('Expected COMPARISSON')
        COMPARISSON_type = tknizer.next.value
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name2 = tknizer.next.value
        name2 = Identifier(name2, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.NEWLINE:
            raise Exception('Expected newline')
        tknizer.select_next()
        result = []
        while tknizer.next.type != Tkn.type.CONCLUDE and tknizer.next.type != Tkn.type.EOF:
            result.append(Prsr.parse_statement(tknizer, symbol_table))
        if tknizer.next.type != Tkn.type.CONCLUDE:
            raise Exception('Expected conclude')
        tknizer.select_next()
        COMPARISSON_node = COMPARISSON(name, name2, COMPARISSON_type)
        return Event(result, COMPARISSON_node, symbol_table)
    

    @staticmethod
    def parse_rain(tknizer, symbol_table):
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.PAREN_OPEN:
            raise Exception('Expected (')
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.PAREN_CLOSE:
            raise Exception('Expected )')
        tknizer.select_next()
        return Rain(name, symbol_table)
    
    @staticmethod
    def parse_dry(tknizer, symbol_table):
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.PAREN_OPEN:
            raise Exception('Expected (')
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.PAREN_CLOSE:
            raise Exception('Expected )')
        tknizer.select_next()
        return Dry(name, symbol_table)
    
    @staticmethod
    def parse_extinguish(tknizer, symbol_table):
        tknizer.select_next()
        if tknizer.next.type != Tkn.type.IDENTIFIER:
            raise Exception('Expected identifier')
        name = tknizer.next.value
        tknizer.select_next()
        return Extinguish(name, symbol_table)
    

    @staticmethod
    def parse_operation(tknizer, symbol_table, name):
        if tknizer.next.type == Tkn.type.BRANCH:
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.NUMBER:
                raise Exception('Expected number')
            value = int(tknizer.next.value)
            tknizer.select_next()
            return Branch(value, name, symbol_table)
        if tknizer.next.type == Tkn.type.ACUMULATE:
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.NUMBER:
                raise Exception('Expected number')
            value = int(tknizer.next.value)
            tknizer.select_next()
            return Acumulate(value, name, symbol_table)
        if tknizer.next.type == Tkn.type.FLOW:
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.NUMBER:
                raise Exception('Expected number')
            value = int(tknizer.next.value)
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.FLOW:
                raise Exception('Expected Flow')
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.IDENTIFIER:
                raise Exception('Expected identifier')
            name2 = tknizer.next.value
            name2 = Identifier(name2, symbol_table)
            tknizer.select_next()
            return Flow(value, name, name2, symbol_table)
        if tknizer.next.type == Tkn.type.ARROW:
            tknizer.select_next()
            if tknizer.next.type != Tkn.type.IDENTIFIER:
                raise Exception('Expected identifier')
            name2 = tknizer.next.value
            name2 = Identifier(name2, symbol_table)
            tknizer.select_next()
            return Arrow(name, name2, symbol_table)
        raise Exception('Invalid operation')
    
        
    @staticmethod       
    def parse_block(tknizer, symbol_table):
        result = NoOp()
        while tknizer.next.type != Tkn.type.EOF:
            #print("teste: ",result)
            result = Statement(result, Prsr.parse_statement(tknizer, symbol_table))
        #print("testeF: ",result)
        return result
    


        
    
    @staticmethod
    def run(source):
        tknizer = Tknizer(source, 0, None)
        symbol_table = Symbol_Table()
        tknizer.select_next() # select first token
        return Prsr.parse_block(tknizer, symbol_table)

    
