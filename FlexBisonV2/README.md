# How to Run Flex/Bison for this project

## Requirements
- Flex
- Bison
- GCC

## How to Run
1. Run the following command to generate the C files from the Flex and Bison files:
```bash
bison -d parser.y
flex lexer.l
```

2. Compile the generated C files:
```bash
gcc -o run parser.tab.c lex.yy.c -lfl
```

3. Run the compiled file:
```bash
./run
```

