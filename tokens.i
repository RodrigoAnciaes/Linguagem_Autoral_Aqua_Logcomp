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
"acumulate"             TOKEN(TACUMULATE); return TACUMULATE;
"branch"                TOKEN(TBRANCH); return TBRANCH;
"conclude"              TOKEN(TCONCLUDE); return TCONCLUDE;
"discover"              TOKEN(TDISCOVER); return TDISCOVER;
"dry"                   TOKEN(TDRY); return TDRY;
"event"                 TOKEN(TEVENT); return TEVENT;
"extinguish"            TOKEN(TEXTINGUISH); return TEXTINGUISH;
"fish"                  TOKEN(TFISH); return TFISH;
"pass_time"             TOKEN(TPASSTIME); return TPASSTIME;
"rain"                  TOKEN(TRAIN); return TRAIN;
"river"                 TOKEN(TRIVER); return TRIVER;
"sustains"              TOKEN(TSUSTAINS); return TSUSTAINS;
"("                     TOKEN(TLPAREN); return TLPAREN;
")"                     TOKEN(TRPAREN); return TRPAREN;
[a-zA-Z_][a-zA-Z0-9_]*  SAVE_TOKEN; return TIDENTIFIER;
[0-9]+                  SAVE_TOKEN; return TINTEGER;
.                       printf("Unknown token!n"); yyterminate();

%%

int yywrap() {
    return 1;
}