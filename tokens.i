%{
#include <string>
#include "node.h"
#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" int yywrap() { }
%}

%%

[ \t\n]                 ;
">>"                    TOKEN(TFLOW); return TFLOW;
"->"                    TOKEN(TPREDATE); return TPREDATE;
"branch"                TOKEN(TBRANCH); return TBRANCH;
"acumulate"             TOKEN(TACUMULATE); return TACUMULATE;
"fish"                  TOKEN(TFISH); return TFISH;
"river"                 TOKEN(TRIVER); return TRIVER;
[a-zA-Z_][a-zA-Z0-9_]*  SAVE_TOKEN; return TIDENTIFIER;
[0-9]+                  SAVE_TOKEN; return TINTEGER;
"dry"                   TOKEN(TDRY); return TDRY;
"extinguish"            TOKEN(TEXTINGUISH); return TEXTINGUISH;
"rain"                  TOKEN(TRAIN); return TRAIN;
"event"                 TOKEN(TEVENT); return TEVENT;
"conclude"              TOKEN(TCONCLUDE); return TCONCLUDE;
"sustains"              TOKEN(TSUSTAINS); return TSUSTAINS;
"pass_time"             TOKEN(TPASSTIME); return TPASSTIME;
"discover"              TOKEN(TDISCOVER); return TDISCOVER;
"("                    TOKEN(TLPAREN); return TLPAREN;
")"                    TOKEN(TRPAREN); return TRPAREN;
.                       printf("Unknown token!n"); yyterminate();

%%