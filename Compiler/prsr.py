
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
        pass
        
    @staticmethod       
    def parse_block(tknizer, symbol_table):
        result = NoOp()
        while tknizer.next.type != Tkn.type.EOF:
            result = Statement(result, Prsr.parse_statement(tknizer, symbol_table))
        #print("testeF: ",result)
        return result
    


        
    
    @staticmethod
    def run(source):
        tknizer = Tknizer(source, 0, None)
        symbol_table = Symbol_Table()
        tknizer.select_next() # select first token
        return Prsr.parse_block(tknizer, symbol_table)

    
