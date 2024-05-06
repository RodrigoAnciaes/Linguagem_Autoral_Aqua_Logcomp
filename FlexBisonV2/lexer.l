%{
#include "parser.tab.h"
%}

/*
EBNF:

BLOCK = { STATEMENT };
STATEMENT = ( "λ" | SPAWN | DISCOVER | SUSTAIN | EVENT | RAIN | DRY | EXTINCTION | OPERATION ), "\n" ;
SPAWN = TYPE, IDENTIFIER, NUMBER, ( "λ" | NUMBER ) ;
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

"branch"               { return BRANCH; }
"acumulate"            { return ACUMULATE; }
"->"                   { return ARROW; }
"river"                { return TYPE; }
"fish"                 { return TYPE; }
"discover"             { return DISCOVER; }
"sustains"             { return SUSTAINS; }
"event"                { return EVENT; }
"conclude"             { return CONCLUDE; }
"rain"                 { return RAIN; }
"dry"                  { return DRY; }
"extinguish"            { return EXTINGUISH; }
"pass_time"            { return PASS_TIME; }


">>"                   { 
                        printf("encontrei >>\n");
                        return FLOW; 
                        }
"("                    { printf("Primeiro parenteses encontrado"); return '('; }
")"                    { return ')'; }
"\n"                   { printf("n\n"); return '\n'; }
[a-zA-Z_]+             { 
                        yylval.string = strdup(yytext); 
                        printf("encontrei string: %s\n", yylval.string);
                        return STRING; 
                        }
[0-9]+                 { yylval.integer = atoi(yytext); return NUMBER; }
[ \t]+                 ; /* ignore whitespace */

.                      { printf("Unexpected character: %s\n", yytext); }

%%