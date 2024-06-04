
from tknizer import Tknizer
from tkn import Tkn
from node import *
from symbolTable import Symbol_Table


class Prsr(object):

    @staticmethod
    def parse_term(tknizer, symbol_table):
        result = Prsr.parse_factor(tknizer, symbol_table)
        haschar = False

        while tknizer.next.type != Tkn.type.EOF:
            if tknizer.next.type == Tkn.type.OP:
                if tknizer.next.value == '*':
                    tknizer.select_next()
                    right = Prsr.parse_factor(tknizer, symbol_table)
                    result = BinOp('*', result, right)
                elif tknizer.next.value == '/':
                    tknizer.select_next()
                    right = Prsr.parse_factor(tknizer, symbol_table)
                    result = BinOp('/', result, right)
                else:
                    break
            elif tknizer.next.type == Tkn.type.EOF:
                break
            else:
                break
                #raise Exception('A4 : Invalid token {TOKEN} at position {position}'.format(position=(tknizer.position-1), TOKEN = tknizer.next))
        return result
    
    @staticmethod
    def parse_expression(tknizer,symbol_table):
        result = Prsr.parse_term(tknizer, symbol_table)
        while tknizer.next.type != Tkn.type.EOF:
            if tknizer.next.type == Tkn.type.OP:
                if tknizer.next.value == '+':
                    tknizer.select_next()
                    right = Prsr.parse_term(tknizer, symbol_table)
                    result = BinOp('+', result, right)
                elif tknizer.next.value == '-':
                    tknizer.select_next()
                    right = Prsr.parse_term(tknizer, symbol_table)
                    result = BinOp('-', result, right)
                else:
                    break
            elif tknizer.next.type == Tkn.type.DOTDOT:
                tknizer.select_next()
                right = Prsr.parse_term(tknizer, symbol_table)
                result = BinOp('..', result, right)

            elif tknizer.next.type == Tkn.type.EOF:
                break
            else:
                break
        return result
    
    @staticmethod
    def parse_factor(tknizer, symbol_table):
        if tknizer.next.type == Tkn.type.NUM:
            result = IntVal(tknizer.next.value)
            tknizer.select_next()
            return result
        if tknizer.next.type == Tkn.type.STRING:
            result = StrVal(tknizer.next.value)
            tknizer.select_next()
            return result
        
        if tknizer.next.type == Tkn.type.READ:
            tknizer.select_next()
            if tknizer.next.type == Tkn.type.OP and tknizer.next.value == '(':
                tknizer.select_next()
                if tknizer.next.type == Tkn.type.OP and tknizer.next.value == ')':
                    tknizer.select_next()
                    return Read()
                else:
                        raise Exception('B1 : Invalid token at position {position}'.format(position=(tknizer.position-1)))
            else:
                    raise Exception('B2 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
            
        elif tknizer.next.type == Tkn.type.OP:
            if tknizer.next.value == '(':
                tknizer.select_next()
                result = Prsr.BoolExp(tknizer, symbol_table)
                if tknizer.next.type == Tkn.type.OP and tknizer.next.value == ')':
                    tknizer.select_next()
                    #print("teste ): ",tknizer.next.type, tknizer.next.value)
                    return result
                else:
                    raise Exception('C1 : Invalid token at position {position}'.format(position=(tknizer.position-1)))
            if tknizer.next.value == '-':
                tknizer.select_next()
                result = UnOp('-', Prsr.parse_factor(tknizer, symbol_table))
                return result
            if tknizer.next.value == '+':
                tknizer.select_next()
                result = UnOp('+', Prsr.parse_factor(tknizer, symbol_table))
                return result
            if tknizer.next.value == 'not':
                tknizer.select_next()
                result = UnOp('not', Prsr.parse_factor(tknizer, symbol_table))
                return result
            else:
                raise Exception('C2 : Invalid token at position {position}'.format(position=(tknizer.position-1)))
            
        if tknizer.next.type == Tkn.type.ID:
            # get from symbol table
            result = Identifier(tknizer.next.value, symbol_table)
            func_name = tknizer.next.value
            tknizer.select_next()
            if tknizer.next.type == Tkn.type.OP and tknizer.next.value == '(':
                tknizer.select_next()
                args = []
                while tknizer.next.type != Tkn.type.OP and tknizer.next.value != ')':  
                    args.append(Prsr.BoolExp(tknizer, symbol_table))
                    if tknizer.next.type == Tkn.type.COMMA:
                        tknizer.select_next()
                if tknizer.next.type == Tkn.type.OP and tknizer.next.value == ')':
                    tknizer.select_next()
                    return FuncCall(func_name, args, symbol_table)
                else:
                    raise Exception('D5 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
            return result
        else:
            raise Exception('C3 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))

    @staticmethod   
    def parse_statement(tknizer, symbol_table):
        #print("teste_s: ",tknizer.next)
        if tknizer.next.type == Tkn.type.FUNCTION:
            #print("teste_func: ",tknizer.next)
            function_symbol_table = Symbol_Table()
            # lua function
            tknizer.select_next()
            if tknizer.next.type == Tkn.type.ID:
                #print("teste_id_func: ",tknizer.next)
                id = tknizer.next.value
                tknizer.select_next()
                if tknizer.next.type == Tkn.type.OP and tknizer.next.value == '(':
                    tknizer.select_next()
                    args = []
                    while tknizer.next.type != Tkn.type.OP and tknizer.next.value != ')':
                        if tknizer.next.type == Tkn.type.ID:
                            args.append(tknizer.next.value)
                            tknizer.select_next()
                            if tknizer.next.type == Tkn.type.COMMA:
                                tknizer.select_next()
                        else:
                            raise Exception('D2 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
                    if tknizer.next.type == Tkn.type.OP and tknizer.next.value == ')':
                        tknizer.select_next()
                        lines = []
                        while tknizer.next.type != Tkn.type.END and tknizer.next.type != Tkn.type.EOF:
                            lines.append(Prsr.parse_statement(tknizer, function_symbol_table))
                        if tknizer.next.type == Tkn.type.END:
                            tknizer.select_next()
                            # add to symbol table
                            return FuncDec(id, args, lines, function_symbol_table, symbol_table)
                    else:
                        raise Exception('D3 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
                else:
                    raise Exception('D4 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
 
                
        if tknizer.next.type == Tkn.type.RETURN:
            tknizer.select_next()
            expr = Prsr.BoolExp(tknizer, symbol_table)
            #print("teste_return: ",expr)
            return Return(expr, symbol_table)

        if tknizer.next.type == Tkn.type.ID:
            #print("teste_id: ",tknizer.next)
            id = tknizer.next.value
            tknizer.select_next()
            #print("teste_id2: ",tknizer.next)
            if tknizer.next.type == Tkn.type.ASSIGN:
                tknizer.select_next()
                #print("teste_id3: ",tknizer.next)
                expr = Prsr.BoolExp(tknizer, symbol_table)
                # add to symbol table
                return Assignement(id, expr, symbol_table)
            elif tknizer.next.type == Tkn.type.OP and tknizer.next.value == '(':
                tknizer.select_next()
                args = []
                while tknizer.next.type != Tkn.type.OP and tknizer.next.value != ')':
                    args.append(Prsr.BoolExp(tknizer, symbol_table))
                    if tknizer.next.type == Tkn.type.COMMA:
                        tknizer.select_next()
                if tknizer.next.type == Tkn.type.OP and tknizer.next.value == ')':
                    tknizer.select_next()
                    return FuncCall(id, args, symbol_table)
                else:
                    raise Exception('D1 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
        if tknizer.next.type == Tkn.type.LOCAL:
            tknizer.select_next()
            if tknizer.next.type == Tkn.type.ID:
                id = tknizer.next.value
                tknizer.select_next()
                if tknizer.next.type == Tkn.type.ASSIGN:
                    tknizer.select_next()
                    expr = Prsr.BoolExp(tknizer, symbol_table)
                    # add to symbol table
                    return VarDeclaration(symbol_table, id, expr)
                else:
                    return VarDeclaration(symbol_table, id, None)
            else:
                raise Exception('E2 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
        if tknizer.next.type == Tkn.type.PRINT:
            tknizer.select_next()
            expr = Prsr.BoolExp(tknizer, symbol_table)
            return Print(expr)
        if tknizer.next.type == Tkn.type.IF:
            tknizer.select_next()
            condition = Prsr.BoolExp(tknizer, symbol_table)
            if tknizer.next.type == Tkn.type.THEN:
                lines = []
                tknizer.select_next()
                while tknizer.next.type != Tkn.type.ELSE and tknizer.next.type != Tkn.type.END and tknizer.next.type != Tkn.type.EOF:
                    lines.append(Prsr.parse_statement(tknizer, symbol_table))
                if tknizer.next.type == Tkn.type.ELSE:
                    tknizer.select_next()
                    else_lines = []
                    while tknizer.next.type != Tkn.type.END and tknizer.next.type != Tkn.type.EOF:
                        else_lines.append(Prsr.parse_statement(tknizer, symbol_table))
                    if tknizer.next.type == Tkn.type.END:
                        tknizer.select_next()
                        return If(condition, lines, else_lines)
                if tknizer.next.type == Tkn.type.END:
                    tknizer.select_next()
                    return If(condition, lines, [])
            else:
                raise Exception('E1 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))

        if tknizer.next.type == Tkn.type.WHILE:
            tknizer.select_next()
            condition = Prsr.BoolExp(tknizer, symbol_table)
            if tknizer.next.type == Tkn.type.DO:
                lines = []
                tknizer.select_next()
                while tknizer.next.type != Tkn.type.END and tknizer.next.type != Tkn.type.EOF:
                    lines.append(Prsr.parse_statement(tknizer, symbol_table))
                if tknizer.next.type == Tkn.type.END:
                    tknizer.select_next()
                    return While(condition, lines)
            else:
                raise Exception('F1 : Invalid token at position {position}'.format(position=(tknizer.position-1)))

        else:
            raise Exception('F2 : Invalid token {token} at position {position}'.format(position=(tknizer.position-1), token = tknizer.next))
        
    @staticmethod       
    def parse_block(tknizer, symbol_table):
        result = NoOp()
        while tknizer.next.type != Tkn.type.EOF:
            result = Statement(result, Prsr.parse_statement(tknizer, symbol_table))
        #print("testeF: ",result)
        return result
    
    @staticmethod
    def RelExp(tknizer, symbol_table):
        result = Prsr.parse_expression(tknizer, symbol_table)
        if tknizer.next.type == Tkn.type.OP:
            if tknizer.next.value == '<':
                tknizer.select_next()
                right = Prsr.parse_expression(tknizer, symbol_table)
                result = BinOp('<', result, right)
            elif tknizer.next.value == '>':
                tknizer.select_next()
                right = Prsr.parse_expression(tknizer, symbol_table)
                result = BinOp('>', result, right)
            elif tknizer.next.value == '==':
                tknizer.select_next()
                right = Prsr.parse_expression(tknizer, symbol_table)
                result = BinOp('==', result, right)
        return result
    
    @staticmethod
    def BoolTerm(tknizer, symbol_table):
        result = Prsr.RelExp(tknizer, symbol_table)
        while tknizer.next.type != Tkn.type.EOF:
            if tknizer.next.type == Tkn.type.OP:
                if tknizer.next.value == 'and':
                    tknizer.select_next()
                    right = Prsr.RelExp(tknizer, symbol_table)
                    result = BinOp('and', result, right)
                else:
                    break
            else:
                break
        return result
    
    @staticmethod
    def BoolExp(tknizer, symbol_table):
        result = Prsr.BoolTerm(tknizer, symbol_table)
        while tknizer.next.type != Tkn.type.EOF:
            if tknizer.next.type == Tkn.type.OP:
                if tknizer.next.value == 'or':
                    tknizer.select_next()
                    right = Prsr.BoolTerm(tknizer, symbol_table)
                    result = BinOp('or', result, right)
                else:
                    break
            else:
                break
        return result
        
    
    @staticmethod
    def run(source):
        tknizer = Tknizer(source, 0, None)
        symbol_table = Symbol_Table()
        tknizer.select_next() # select first token
        return Prsr.parse_block(tknizer, symbol_table)

    
