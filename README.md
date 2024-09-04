# Aqua Joke Language

## Official documentation:

https://rodrigoanciaes.github.io/Aqua-Documentation/

## Compiler and examples

The compiler and code examples can be found in the Compiler folder.

## Presentation

Presentation slides: [Slides](docs/Apresentacao_Linguagem_de_Programação_Aqua.pdf)

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

## Syntax Diagram

![Syntax Diagram](DiagramaSintatico.png)

## Introduction

The Aqua language, developed for the Computational Logic course, is a joke language that simulates the natural world through code. To program in this language, it is necessary to create sets of rivers and fish and define the relationships between them. The language consists of two types of declarations: river declarations and fish declarations.

Note: The language does not require indentation, but it is recommended for better code readability.

A commented example of code in Aqua is:

```
river x create 10 -- creates a river with 10 units of water

river y create 10

x >> 5 >> y -- River x transfers 5 units of water to river y
discover(x) -- prints 5
discover(y) -- prints 15

x branch 5 -- River x splits into 5 rivers
discover(x) -- prints 1
y >> 1 >> x -- River y transfers 1 unit of water to river x
x accumulate 5 -- x = x * 5 (river x accumulates 5 times the amount of water it has)

fish z create 2,1 -- creates a population of 2 that consumes 1 per individual
fish f create 1,1 -- creates a population of 1 that consumes 1 per individual

x sustains z: -- while x sustains z  
-- to sustain z, x must be greater than 0, and z consumes (reduces the value of) x by the amount of its (z_consumption * z_population) and increases its number by (z_population = z_population + (z_population - z_population % 2) + sub)
-- sub = dif if dif > 0 else 0
-- dif = x_population - z_population * z_consumption  
y >> 1 >> x:
f -> z -- f consumes z to increase its number in the same way as sustains  
event z inf f -- if the population of z is less than f, an event is triggered  
extinguish f -- f is extinguished (delete f)  
conclude -- end of event  
pass_time -- time passes (the loop restarts)

rain(y) -- all rivers receive a water value equivalent to the amount in y

dry(x) -- all rivers lose a water value equivalent to the amount in x
```

A clean example of code in Aqua is:

```
river x create 10
river y create 10
x >> 5 >> y
discover(x)
discover(y)
x branch 5
discover(x)
y >> 1 >> x
x accumulate 5
fish z create 2,1
fish f create 1,1
x sustains z:
y >> 1 >> x:
f -> z   
event z inf f 
extinguish f
conclude
pass_time
rain(y)
dry(x)
```