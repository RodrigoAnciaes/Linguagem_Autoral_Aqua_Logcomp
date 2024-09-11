"""
    This module contains the parser class which is responsible for parsing the source code.
"""

from tknizer import Tknizer
from tkn import Tkn
from node import (Node,Identifier,Create,Discover,Flow,
                  Acumulate,Arrow,Sustains,Event,Rain,Dry,NoOp,
                  Statement,COMPARISSON,Extinguish,Branch)
from symbol_table import SymbolTable


class Prsr():
    """
    Parses statements and constructs objects based on the token stream.
    Attributes:
        None
    Methods:
        parse_statement(tknizer, symbol_table): Parses a statement from the token stream.
        parse_spawn(tknizer, symbol_table): Parses the spawn statement from the token stream.
        parse_discover(tknizer, symbol_table): Parses the 'discover' statement.
        parse_sustains(tknizer, symbol_table, name): Parses the 'sustains' statement.
        parse_event(tknizer, symbol_table): Parses an event from the token stream.
        parse_rain(tknizer, symbol_table): Parses the 'rain' production rule.
        parse_dry(tknizer, symbol_table): Parses a 'dry' statement from the token stream.
        parse_extinguish(tknizer, symbol_table): Parses the 'extinguish' statement.
        parse_operation(tknizer, symbol_table, name): 
        Parses the next operation from the tokenizer and returns the corresponding object.
        parse_block(tknizer, symbol_table): 
        Parses a block of statements from the given tokenizer and symbol table.
        run(source): Runs the parser on the given source code.
    """
    @staticmethod
    def parse_statement(tknizer, symbol_table):
        """
        Parses a statement from the token stream.

        Args:
            tknizer (Tknizer): The tokenizer object.
            symbol_table (SymbolTable): The symbol table object.

        Returns:
            Statement: The parsed statement.

        Raises:
            ValueError: If an unexpected token is encountered
            or if a newline is expected but not found.
        """
        # print("teste: ",tknizer.next.type)
        if tknizer.next.type in (Tkn.Type.EOF,Tkn.Type.NEWLINE):
            tknizer.select_next()
            return NoOp()
        if tknizer.next.type in(Tkn.Type.FISH,Tkn.Type.RIVER):
            result = Prsr.parse_spawn(tknizer, symbol_table)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF):
                raise ValueError("Expected newline")
            return result
        if tknizer.next.type == Tkn.Type.DISCOVER:
            result = Prsr.parse_discover(tknizer, symbol_table)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF):
                raise ValueError("Expected newline")
            return result
        if tknizer.next.type == Tkn.Type.EVENT:
            result = Prsr.parse_event(tknizer, symbol_table)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF):
                raise ValueError("Expected newline")
            return result
        if tknizer.next.type == Tkn.Type.RAIN:
            result = Prsr.parse_rain(tknizer, symbol_table)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF):
                raise ValueError("Expected newline")
            return result
        if tknizer.next.type == Tkn.Type.DRY:
            result = Prsr.parse_dry(tknizer, symbol_table)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF) :
                raise ValueError("Expected newline")
            return result
        if tknizer.next.type == Tkn.Type.EXTINGUISH:
            result = Prsr.parse_extinguish(tknizer, symbol_table)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF):
                raise ValueError("Expected newline")
            return result
        if tknizer.next.type == Tkn.Type.IDENTIFIER:
            name = tknizer.next.value
            name = Identifier(name, symbol_table)
            tknizer.select_next()
            if tknizer.next.type == Tkn.Type.SUSTAINS:
                result = Prsr.parse_sustains(tknizer, symbol_table, name)
            else:
                result = Prsr.parse_operation(tknizer, symbol_table, name)
            if tknizer.next.type not in (Tkn.Type.NEWLINE,Tkn.Type.EOF):
                raise ValueError("Expected newline")
            return result

    @staticmethod
    def parse_spawn(tknizer, symbol_table):
        """
        Parses the spawn statement from the token stream.

        Args:
            tknizer (Tokenizer): The tokenizer object used to tokenize the input.
            symbol_table (SymbolTable): The symbol table used for symbol lookup.

        Returns:
            Create: The Create object representing the spawn statement.

        Raises:
            ValueError: If the expected tokens are not found in the token stream.
        """
        my_type = ""
        if tknizer.next.type == Tkn.Type.FISH:
            my_type = "fish"
        else:
            my_type = "river"
        tknizer.select_next()
        name = tknizer.next.value
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.CREATE:
            raise ValueError("Expected create")
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.NUMBER:
            raise ValueError("Expected number")
        value = int(tknizer.next.value)
        tknizer.select_next()
        if tknizer.next.type == Tkn.Type.COMMA:
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.NUMBER:
                raise ValueError("Expected number")
            value2 = int(tknizer.next.value)
            tknizer.select_next()
        else:
            value2 = 0
            # tknizer.select_next()
        return Create(name, value, value2, symbol_table, my_type)

    @staticmethod
    def parse_discover(tknizer, symbol_table):
        """
        Parses the 'discover' statement.

        Args:
            tknizer (Tokenizer): The tokenizer object.
            symbol_table (SymbolTable): The symbol table object.

        Returns:
            Discover: The parsed 'discover' statement.

        Raises:
            ValueError: If the expected tokens are not found.
        """
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.PAREN_OPEN:
            raise ValueError("Expected (")
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.PAREN_CLOSE:
            raise ValueError("Expected )")
        tknizer.select_next()
        return Discover(name)

    @staticmethod
    def parse_sustains(tknizer, symbol_table, name):
        """
        Parses the 'sustains' statement.

        Args:
            tknizer (Tknizer): The tokenizer object.
            symbol_table (SymbolTable): The symbol table object.
            name (str): The name of the 'sustains' statement.

        Returns:
            Sustains: The parsed 'sustains' statement.

        Raises:
            ValueError: If an expected identifier or newline is not found.
        """
        # Code implementation goes here
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name2 = tknizer.next.value
        name2 = Identifier(name2, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.NEWLINE:
            raise ValueError("Expected newline")
        tknizer.select_next()
        result = []
        while tknizer.next.type not in (Tkn.Type.PASS_TIME,Tkn.Type.EOF):
            result.append(Prsr.parse_statement(tknizer, symbol_table))
        if tknizer.next.type != Tkn.Type.PASS_TIME:
            raise ValueError("Expected pass_time")
        tknizer.select_next()
        return Sustains(result, name, name2, symbol_table)

    @staticmethod
    def parse_event(tknizer, symbol_table):
        """
        Parses an event from the token stream.

        Args:
            tknizer (Tokenizer): The tokenizer object used to tokenize the input.
            symbol_table (SymbolTable): The symbol table used for identifier lookup.

        Returns:
            Event: The parsed event object.

        Raises:
            ValueError: If the expected tokens are not found in the token stream.
        """
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.COMPARISSON:
            raise ValueError("Expected COMPARISSON")
        comparisson_type = tknizer.next.value
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name2 = tknizer.next.value
        name2 = Identifier(name2, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.NEWLINE:
            raise ValueError("Expected newline")
        tknizer.select_next()
        result = []
        while tknizer.next.type not in(Tkn.Type.CONCLUDE,Tkn.Type.EOF):
            result.append(Prsr.parse_statement(tknizer, symbol_table))
        if tknizer.next.type != Tkn.Type.CONCLUDE:
            raise ValueError("Expected conclude")
        tknizer.select_next()
        comparissom_node = COMPARISSON(name, name2, comparisson_type)
        return Event(result, comparissom_node, symbol_table)

    @staticmethod
    def parse_rain(tknizer, symbol_table):
        """
        Parses the 'rain' production rule.

        Args:
            tknizer (Tknizer): The tokenizer object.
            symbol_table (SymbolTable): The symbol table object.

        Returns:
            Rain: The parsed Rain object.

        Raises:
            ValueError: If the expected tokens are not found.
        """
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.PAREN_OPEN:
            raise ValueError("Expected (")
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.PAREN_CLOSE:
            raise ValueError("Expected )")
        tknizer.select_next()
        return Rain(name, symbol_table)

    @staticmethod
    def parse_dry(tknizer, symbol_table):
        """
        Parses a 'dry' statement from the token stream.

        Args:
            tknizer (Tokenizer): The tokenizer object used to iterate through the tokens.
            symbol_table (SymbolTable): The symbol table used for storing identifiers.

        Returns:
            Dry: The parsed 'dry' statement.

        Raises:
            ValueError: If the expected tokens are not found in the token stream.
        """
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.PAREN_OPEN:
            raise ValueError("Expected (")
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name = tknizer.next.value
        name = Identifier(name, symbol_table)
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.PAREN_CLOSE:
            raise ValueError("Expected )")
        tknizer.select_next()
        return Dry(name, symbol_table)

    @staticmethod
    def parse_extinguish(tknizer, symbol_table):
        """
        Parses the 'extinguish' statement.

        Args:
            tknizer (Tokenizer): The tokenizer object.
            symbol_table (SymbolTable): The symbol table object.

        Returns:
            Extinguish: The Extinguish object.

        Raises:
            ValueError: If the next token is not an identifier.
        """
        tknizer.select_next()
        if tknizer.next.type != Tkn.Type.IDENTIFIER:
            raise ValueError("Expected identifier")
        name = tknizer.next.value
        tknizer.select_next()
        return Extinguish(name, symbol_table)

    @staticmethod
    def parse_operation(tknizer, symbol_table, name):
        """
        Parses the next operation from the tokenizer and returns the corresponding object.

        Args:
            tknizer (Tokenizer): The tokenizer object used to tokenize the input.
            symbol_table (SymbolTable): The symbol table used for storing identifiers.
            name (str): The name of the operation.

        Returns:
            Operation: The parsed operation object.

        Raises:
            ValueError: If the operation is invalid or if the expected tokens are not found.
        """
        if tknizer.next.type == Tkn.Type.BRANCH:
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.NUMBER:
                raise ValueError("Expected number")
            value = int(tknizer.next.value)
            tknizer.select_next()
            return Branch(value, name, symbol_table)
        if tknizer.next.type == Tkn.Type.ACUMULATE:
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.NUMBER:
                raise ValueError("Expected number")
            value = int(tknizer.next.value)
            tknizer.select_next()
            return Acumulate(value, name, symbol_table)
        if tknizer.next.type == Tkn.Type.FLOW:
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.NUMBER:
                raise ValueError("Expected number")
            value = int(tknizer.next.value)
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.FLOW:
                raise ValueError("Expected Flow")
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.IDENTIFIER:
                raise ValueError("Expected identifier")
            name2 = tknizer.next.value
            name2 = Identifier(name2, symbol_table)
            tknizer.select_next()
            return Flow(value, name, name2, symbol_table)
        if tknizer.next.type == Tkn.Type.ARROW:
            tknizer.select_next()
            if tknizer.next.type != Tkn.Type.IDENTIFIER:
                raise ValueError("Expected identifier")
            name2 = tknizer.next.value
            name2 = Identifier(name2, symbol_table)
            tknizer.select_next()
            return Arrow(name, name2, symbol_table)
        raise ValueError("Invalid operation")

    @staticmethod
    def parse_block(tknizer, symbol_table):
        """
        Parses a block of statements from the given tokenizer and symbol table.

        Args:
            tknizer (Tokenizer): The tokenizer object used to tokenize the input.
            symbol_table (SymbolTable): The symbol table object used to store and retrieve symbols.

        Returns:
            Statement: The parsed block of statements.

        """
        result = NoOp()
        while tknizer.next.type != Tkn.Type.EOF:
            # print("teste: ",result)
            result = Statement(
                result, Prsr.parse_statement(tknizer, symbol_table))
        # print("testeF: ",result)
        return result

    @staticmethod
    def run(source):
        """
        Runs the parser on the given source code.

        Args:
            source (str): The source code to be parsed.

        Returns:
            object: The result of parsing the source code.
        """
        tknizer = Tknizer(source, 0, None)
        symbol_table = SymbolTable()
        tknizer.select_next()  # select first token
        return Prsr.parse_block(tknizer, symbol_table)
