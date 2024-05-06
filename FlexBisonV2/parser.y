%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

void yyerror(const char *s);
extern int yylex();

typedef struct {
    char *name;
    int time;
} Task;

Task tasks[100];
int numTasks = 0;

/* Function to find task by name */
Task* findTaskByName(const char *name) {
    for (int i = 0; i < numTasks; ++i) {
        if (strcmp(tasks[i].name, name) == 0) {
            return &tasks[i];
        }
    }
    return NULL;
}

%}


%union {
    char *string;
    int integer;
}

/*
EBNF:
BLOCK = { STATEMENT };
STATEMENT = ( "λ" | SPAWN | DISCOVER | SUSTAIN | EVENT | RAIN | DRY | EXTINCTION | OPERATION ), "\n" ;
SPAWN = TYPE, IDENTIFIER, "create", ( "λ" | NUMBER ) ;
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
%token <string> BRANCH ACUMULATE ARROW FLOW TYPE DISCOVER SUSTAINS EVENT RAIN DRY EXTINGUISH OPERATION PASS_TIME CONCLUDE CREATE

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


spawn: TYPE STRING CREATE NUMBER
    | TYPE STRING CREATE
    ;

discover: DISCOVER '(' STRING ')'
    ;

sustaining: sustaining statement
    | statement

sustain: STRING SUSTAINS STRING '\n' sustaining PASS_TIME
    ;

statements: statements statement
    | statement

event: EVENT STRING STRING STRING '\n' statements CONCLUDE

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
    | STRING FLOW NUMBER FLOW NUMBER

%%

void yyerror(const char *s) {
    fprintf(stderr, "%s\n", s);
}

int main() {
    printf("Digite o programa:\n");
    if (yyparse() == 0) {
        printf("Programa aceito\n");
    } else {
        printf("Programa rejeitado\n");
    }
    return 0;
}

