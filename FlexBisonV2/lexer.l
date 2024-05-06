%{
#include "parser.tab.h"
%}

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


%%


"inf"                 { printf("encontrei inferior\n");
                        return COMPARISSON; }
"sup"                 { printf("encontrei superior\n");
                        return COMPARISSON; }
"ig"                  { printf("encontrei igual\n");
                        return COMPARISSON; }

","                    { printf("encontrei virgula\n");
                        return ','; }
"create"               { printf("encontrei create\n");
                        return CREATE; }
"branch"               { printf("encontrei branch\n");
                        return BRANCH; }
"acumulate"            { printf("encontrei acumulate\n");
                        return ACUMULATE; }
"->"                   { printf("encontrei ->\n");
                        return ARROW; }
"river"                { printf("encontrei river\n");
                        return RIVER; }
"fish"                 { printf("encontrei fish\n");
                        return FISH; }
"discover"             { printf("encontrei discover\n");
                        return DISCOVER; }
"sustains"             { printf("encontrei sustains\n");
                        return SUSTAINS; }
"event"                { printf("encontrei event\n");
                        return EVENT; }
"conclude"             { printf("encontrei conclude\n");
                        return CONCLUDE; }
"rain"                 { printf("encontrei rain\n");
                        return RAIN; }
"dry"                  { printf("encontrei dry\n");
                        return DRY; }
"extinguish"            { printf("encontrei extinguish\n");
                        return EXTINGUISH; }
"pass_time"            { printf("encontrei pass_time\n");
                        return PASS_TIME; }

">>"                   { 
                        printf("encontrei >>\n");
                        return FLOW; 
                        }
"("                    { printf("Primeiro parenteses encontrado"); return '('; }
")"                    { return ')'; }
"\n"                   { printf("Enconntrei Barra n\n"); return '\n'; }
[a-zA-Z_]+             { 
                        yylval.string = strdup(yytext); 
                        printf("encontrei string: %s\n", yylval.string);
                        return STRING; 
                        }
[0-9]+                 { yylval.integer = atoi(yytext); 
                        printf("encontrei numero: %d\n", yylval.integer);
                        return NUMBER; }
[ \t]+                 ; /* ignore whitespace */

.                      { printf("Unexpected character: %s\n", yytext); }

%%