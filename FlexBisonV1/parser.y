%{
    #include "node.h"
    NBlock *programBlock; /* the top level root node of our final AST */

    extern int yylex();
    void yyerror(const char *s) { printf("ERROR: %sn", s); }
%}

/* Represents the many different ways we can access our data */
%union {
    /* my nodes*/
    NBlock *block;
    NStatement *stmt;
    NSpawn *spawn;
    NDiscover *discover;
    NSustain *sustain;
    NEvent *event;
    NRain *rain;
    NDry *dry;
    NExtinction *extinction;
    NOperation *operation;
    NIdentifier *identifier;
    NNumber *number;
    NType *type;
    NOperationType *operation_type;
}

/* Define our terminal symbols (tokens). This should
   match our tokens.l lex file. We also define the node type
   they represent.
 */
/*My sybols*/
%token <token> TFLOW TPREDATE TACUMULATE TBRANCH
%token <token> TCONCLUDE TDISCOVER TDRY TEVENT
%token <token> TEXTINGUISH TFISH TPASSTIME TRAIN
%token <token> TRIVER TSUSTAINS TLPAREN TRPAREN

/* Define the type of node our nonterminal symbols represent.
   The types refer to the %union declaration above. Ex: when
   we call an ident (defined by union type ident) we are really
   calling an (NIdentifier*). It makes the compiler happy.
 */
/* my assossiations*/
%type <block> block
%type <stmt> stmt
%type <spawn> spawn
%type <discover> discover
%type <sustain> sustain
%type <event> event
%type <rain> rain
%type <dry> dry
%type <extinction> extinction
%type <operation> operation
%type <identifier> identifier
%type <number> number
%type <type> type
%type <operation_type> operation_type

/* Operator precedence for mathematical operators */
/*My operator procedance*/
%left TFLOW TPREDATE TACUMULATE TBRANCH
%left TDRY TRAIN

%start program

%%

/*EBNF:

BLOCK = { STATEMENT };
STATEMENT = ( "λ" | SPAW | DISCOVER | SUSTAIN | EVENT | RAIN | DRY | EXTINCTION | OPERATION ), "\n" ;
SPAW = TYPE, IDENTIFIER, NUMBER, ( "λ" | NUMBER ) ;
DISCOVER = "discover", "(", IDENTIFIER, ")" ;
SUSTAIN = IDENTIFIER, "sustains", IDENTIFIER, "\n", "λ", { ( STATEMENT ), "λ" }, "pass_time" ;
EVENT = "event", IDENTIFIER, COMPARISSON, IDENTIFIER, "\n", "λ", { ( STATEMENT ), "λ" }, "conclude" ;
RAIN = "rain","(", IDENTIFIER, ")" ;
DRY = "dry","(", IDENTIFIER, ")" ;
EXTINCTION = "extingish", IDENTIFIER ; 
OPERATION = IDENTIFIER, OP_T, NUMBER, ( "λ" | OP_T, IDENTIFIER ) ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( "a" | "..." | "z" | "A" | "..." | "Z" ) ;
DIGIT = ( "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "0" );
TYPE = ( "river" | "fish" ) ;
OP_T = ( "branch" | "acumulate" | ">>" | "->" ) ;
*/

program: block { programBlock = $1; }

block: /* nothing */ { $$ = new NBlock(); }
    | block stmt { $$ = $1; if ($2 != NULL) $1->statements.push_back($2); }

stmt: spawn { $$ = $1; }
    | discover { $$ = $1; }
    | sustain { $$ = $1; }
    | event { $$ = $1; }
    | rain { $$ = $1; }
    | dry { $$ = $1; }
    | extinction { $$ = $1; }
    | operation { $$ = $1; }

spawn: type identifier number { $$ = new NSpawn($1, $2, $3); }

discover: TDISCOVER TLPAREN identifier TRPAREN { $$ = new NDiscover($3); }

sustain: identifier TSUSTAINS identifier '\n' { $$ = new NSustain($1, $3); }
    | identifier TSUSTAINS identifier '\n' block TPASSTIME { $$ = new NSustain($1, $3, $5); }

event: TEVENT identifier operation identifier '\n' { $$ = new NEvent($2, $3, $4); }

rain: TRAIN TLPAREN identifier TRPAREN { $$ = new NRain($3); }

dry: TDRY TLPAREN identifier TRPAREN { $$ = new NDry($3); }

extinction: TEXTINGUISH identifier { $$ = new NExtinction($2); }

operation: identifier operation_type number { $$ = new NOperation($1, $2, $3); }
    | identifier operation_type number operation_type identifier { $$ = new NOperation($1, $2, $3, $4, $5); }

identifier: TIDENTIFIER { $$ = new NIdentifier(*$1); }

number: TNUMBER { $$ = new NNumber(*$1); }

type: TRIVER { $$ = new NType(*$1); }
    | TFISH { $$ = new NType(*$1); }

operation_type: TBRANCH { $$ = new NOperationType(*$1); }
    | TACUMULATE { $$ = new NOperationType(*$1); }
    | TPREDATE { $$ = new NOperationType(*$1); }
    | TFLOW { $$ = new NOperationType(*$1); }




%%