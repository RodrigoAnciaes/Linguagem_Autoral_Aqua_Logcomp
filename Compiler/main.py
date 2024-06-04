
import sys
from prsr import Prsr
from tknizer import Tknizer
from tkn import Tkn
from PrePro import PrePro




def main ():
    arquive = sys.argv[1]
    # abre o arquivo .lua
    with open(arquive, 'r') as file:
        string = file.read()
    
    string = PrePro.filter(string)
    #print(string)
    AST = Prsr.run(string)
    #print('ASTb: ', AST)
    AST = AST.evaluate()
    #print("ASTa: ",AST)
    pass

    

if __name__ == "__main__":
    main()

    

