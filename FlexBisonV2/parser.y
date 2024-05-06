%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

void yyerror(const char *s);
extern int yylex();

%}


%union {
    char *string;
    int integer;
}

/*
EBNF:
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
*/

%token <string> STRING
%token <integer> NUMBER
%token <string> BRANCH ACUMULATE ARROW FLOW RIVER FISH DISCOVER SUSTAINS EVENT RAIN DRY EXTINGUISH OPERATION PASS_TIME CONCLUDE CREATE COMPARISSON

%%


block: statements
    ;


statement: spawn '\n'
    | discover '\n'
    | sustain '\n'
    | event '\n'
    | rain '\n'
    | dry '\n'
    | extinguish '\n'
    | operation '\n'
    | '\n'
    ;


spawn: RIVER STRING CREATE NUMBER
    | RIVER STRING CREATE
    | FISH STRING CREATE NUMBER ',' NUMBER
    | FISH STRING CREATE
    ;

discover: DISCOVER '(' STRING ')'
    ;


sustain: STRING SUSTAINS STRING '\n' PASS_TIME
    | STRING SUSTAINS STRING '\n' statements PASS_TIME
    ;

statements: statements statement
    | statement
    ;

event: EVENT STRING COMPARISSON STRING '\n' CONCLUDE
    | EVENT STRING COMPARISSON STRING '\n' statements CONCLUDE
    ;

rain: RAIN '(' STRING ')'
    ;

dry: DRY '(' STRING ')'
    ;

extinguish: EXTINGUISH STRING
    ;

operation: STRING BRANCH NUMBER
    | STRING BRANCH STRING
    | STRING ACUMULATE NUMBER
    | STRING ACUMULATE STRING
    | STRING ARROW NUMBER
    | STRING ARROW STRING
    | STRING FLOW NUMBER FLOW STRING

%%

void yyerror(const char *s) {
    fprintf(stderr, "%s\n", s);
}

int main() {
    printf("Digite o programa:\n");
    if (yyparse() == 0) {
        printf("Programa aceito pelo parser\n");
    } else {
        printf("Programa rejeitado pelo parser\n");
    }
    return 0;
}

