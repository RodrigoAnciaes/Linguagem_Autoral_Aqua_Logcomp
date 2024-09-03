# How to Run Flex/Bison for this project

## Requirements
- Flex (utilized version = flex 2.6.4)
- Bison (utilized version = bison (GNU Bison) 3.8.2)
- GCC   (utilized version = gcc (Debian 13.2.0-23) 13.2.0)

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

