"""
Module: tknizer
Description: This module defines the Tknizer class, which is responsible for tokenizing
             a source input into distinct tokens that can be used for parsing.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from Compiler.tkn import Tkn


class Tknizer():
    """
    A class representing a tokenizer that processes an input source into tokens.
    """

    def __init__(self, source, position, next_):
        self.source = source
        self.position = position
        self.next = next_
        if len(self.source) == 0:
            raise ValueError("source cannot be None")

    def select_next(self):
        """
        Selects the next token in the source string.

        Returns:
            Tkn: The next token in the source.

        Raises:
            ValueError: If an invalid character is encountered in the source.
        """
        if self.position >= len(self.source):
            self.next = Tkn(Tkn.Type.EOF, None)
            return self.next
        while self.source[self.position] in [" ", "\t", "\r"]:
            self.position += 1
            if self.position >= len(self.source):
                self.next = Tkn(Tkn.Type.EOF, None)
                return next
        # \n
        if self.source[self.position] == "\n":
            self.position += 1
            self.next = Tkn(Tkn.Type.NEWLINE, "\n")
            return self.next
        # NUMBER
        if self.source[self.position].isdigit():
            start = self.position
            while (
                self.position < len(self.source)
                and self.source[self.position].isdigit()
            ):
                self.position += 1
            self.next = Tkn(Tkn.Type.NUMBER, int(self.source[start : self.position]))
            return self.next
        # COMMA
        if self.source[self.position] == ",":
            self.next = Tkn(Tkn.Type.COMMA, ",")
            self.position += 1
            return self.next
        # PAREN_OPEN
        if self.source[self.position] == "(":
            self.next = Tkn(Tkn.Type.PAREN_OPEN, "(")
            self.position += 1
            return self.next
        # PAREN_CLOSE
        if self.source[self.position] == ")":
            self.next = Tkn(Tkn.Type.PAREN_CLOSE, ")")
            self.position += 1
            return self.next
        ## RESERVED WORDS SECTION ##

        # COMPARISSON (inf, sup, ig)

        # inf ( a inf b)
        if self.source[self.position] == "i":
            if (
                self.position + 3 < len(self.source)
                and self.source[self.position : self.position + 3] == "inf"
            ):
                self.next = Tkn(Tkn.Type.COMPARISSON, "inf")
                self.position += 3
                return self.next

        # sup ( a sup b)
        if self.source[self.position] == "s":
            if (
                self.position + 3 < len(self.source)
                and self.source[self.position : self.position + 3] == "sup"
            ):
                self.next = Tkn(Tkn.Type.COMPARISSON, "sup")
                self.position += 3
                return self.next

        # ig ( a ig b)
        if self.source[self.position] == "i":
            if (
                self.position + 2 < len(self.source)
                and self.source[self.position : self.position + 2] == "ig"
            ):
                self.next = Tkn(Tkn.Type.COMPARISSON, "ig")
                self.position += 2
                return self.next

        # create
        if self.source[self.position] == "c":
            if (
                self.position + 6 < len(self.source)
                and self.source[self.position : self.position + 6] == "create"
            ):
                self.next = Tkn(Tkn.Type.CREATE, "create")
                self.position += 6
                return self.next

        # branch
        if self.source[self.position] == "b":
            if (
                self.position + 6 < len(self.source)
                and self.source[self.position : self.position + 6] == "branch"
            ):
                self.next = Tkn(Tkn.Type.BRANCH, "branch")
                self.position += 6
                return self.next

        # acumulate
        if self.source[self.position] == "a":
            if (
                self.position + 9 < len(self.source)
                and self.source[self.position : self.position + 9] == "acumulate"
            ):
                self.next = Tkn(Tkn.Type.ACUMULATE, "acumulate")
                self.position += 9
                return self.next

        # river
        if self.source[self.position] == "r":
            if (
                self.position + 5 < len(self.source)
                and self.source[self.position : self.position + 5] == "river"
            ):
                self.next = Tkn(Tkn.Type.RIVER, "river")
                self.position += 5
                return self.next

        # fish
        if self.source[self.position] == "f":
            if (
                self.position + 4 < len(self.source)
                and self.source[self.position : self.position + 4] == "fish"
            ):
                self.next = Tkn(Tkn.Type.FISH, "fish")
                self.position += 4
                return self.next

        # discover
        if self.source[self.position] == "d":
            if (
                self.position + 8 < len(self.source)
                and self.source[self.position : self.position + 8] == "discover"
            ):
                self.next = Tkn(Tkn.Type.DISCOVER, "discover")
                self.position += 8
                return self.next

        # sustains
        if self.source[self.position] == "s":
            if (
                self.position + 8 < len(self.source)
                and self.source[self.position : self.position + 8] == "sustains"
            ):
                self.next = Tkn(Tkn.Type.SUSTAINS, "sustains")
                self.position += 8
                return self.next

        # event
        if self.source[self.position] == "e":
            if (
                self.position + 5 < len(self.source)
                and self.source[self.position : self.position + 5] == "event"
            ):
                self.next = Tkn(Tkn.Type.EVENT, "event")
                self.position += 5
                return self.next

        # conclude
        if self.source[self.position] == "c":
            if (
                self.position + 7 < len(self.source)
                and self.source[self.position : self.position + 8] == "conclude"
            ):
                self.next = Tkn(Tkn.Type.CONCLUDE, "conclude")
                self.position += 8
                return self.next

        # rain
        if self.source[self.position] == "r":
            if (
                self.position + 4 < len(self.source)
                and self.source[self.position : self.position + 4] == "rain"
            ):
                self.next = Tkn(Tkn.Type.RAIN, "rain")
                self.position += 4
                return self.next

        # dry
        if self.source[self.position] == "d":
            if (
                self.position + 3 < len(self.source)
                and self.source[self.position : self.position + 3] == "dry"
            ):
                self.next = Tkn(Tkn.Type.DRY, "dry")
                self.position += 3
                return self.next

        # extinguish
        if self.source[self.position] == "e":
            if (
                self.position + 10 < len(self.source)
                and self.source[self.position : self.position + 10] == "extinguish"
            ):
                self.next = Tkn(Tkn.Type.EXTINGUISH, "extinguish")
                self.position += 10
                return self.next

        # pass_time
        if self.source[self.position] == "p":
            if (
                self.position + 8 < len(self.source)
                and self.source[self.position : self.position + 9] == "pass_time"
            ):
                self.next = Tkn(Tkn.Type.PASS_TIME, "pass_time")
                self.position += 9
                return self.next

        ## END OF RESERVED WORDS SECTION ##

        # ID
        if self.source[self.position].isalpha():
            start = self.position
            while self.position < len(self.source) and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            ):
                self.position += 1
            self.next = Tkn(Tkn.Type.IDENTIFIER, self.source[start : self.position])
            return self.next

        # ARROW ->
        if self.source[self.position] == "-" and self.source[self.position + 1] == ">":
            self.next = Tkn(Tkn.Type.ARROW, "->")
            self.position += 2
            return self.next

        # FLOW >>
        if self.source[self.position] == ">" and self.source[self.position + 1] == ">":
            self.next = Tkn(Tkn.Type.FLOW, ">>")
            self.position += 2
            return self.next

        raise ValueError(
            f"Invalid character {self.source[self.position]} at position {self.position}")
