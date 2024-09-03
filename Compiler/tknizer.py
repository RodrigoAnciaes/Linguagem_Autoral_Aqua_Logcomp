"""
Module: tknizer
Description: This module defines the Tknizer class, which is responsible for tokenizing
             a source input into distinct tokens that can be used for parsing.
"""

from tkn import Tkn


class Tknizer(object):
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
            self.next = Tkn(Tkn.type.EOF, None)
            return self.next
        while self.source[self.position] in [" ", "\t", "\r"]:
            self.position += 1
            if self.position >= len(self.source):
                self.next = Tkn(Tkn.type.EOF, None)
                return next
        # \n
        if self.source[self.position] == "\n":
            self.position += 1
            self.next = Tkn(Tkn.type.NEWLINE, "\n")
            return self.next
        # NUMBER
        if self.source[self.position].isdigit():
            start = self.position
            while (
                self.position < len(self.source)
                and self.source[self.position].isdigit()
            ):
                self.position += 1
            self.next = Tkn(Tkn.type.NUMBER, int(self.source[start : self.position]))
            return self.next
        # COMMA
        if self.source[self.position] == ",":
            self.next = Tkn(Tkn.type.COMMA, ",")
            self.position += 1
            return self.next
        # PAREN_OPEN
        if self.source[self.position] == "(":
            self.next = Tkn(Tkn.type.PAREN_OPEN, "(")
            self.position += 1
            return self.next
        # PAREN_CLOSE
        if self.source[self.position] == ")":
            self.next = Tkn(Tkn.type.PAREN_CLOSE, ")")
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
                self.next = Tkn(Tkn.type.COMPARISSON, "inf")
                self.position += 3
                return self.next

        # sup ( a sup b)
        if self.source[self.position] == "s":
            if (
                self.position + 3 < len(self.source)
                and self.source[self.position : self.position + 3] == "sup"
            ):
                self.next = Tkn(Tkn.type.COMPARISSON, "sup")
                self.position += 3
                return self.next

        # ig ( a ig b)
        if self.source[self.position] == "i":
            if (
                self.position + 2 < len(self.source)
                and self.source[self.position : self.position + 2] == "ig"
            ):
                self.next = Tkn(Tkn.type.COMPARISSON, "ig")
                self.position += 2
                return self.next

        # create
        if self.source[self.position] == "c":
            if (
                self.position + 6 < len(self.source)
                and self.source[self.position : self.position + 6] == "create"
            ):
                self.next = Tkn(Tkn.type.CREATE, "create")
                self.position += 6
                return self.next

        # branch
        if self.source[self.position] == "b":
            if (
                self.position + 6 < len(self.source)
                and self.source[self.position : self.position + 6] == "branch"
            ):
                self.next = Tkn(Tkn.type.BRANCH, "branch")
                self.position += 6
                return self.next

        # acumulate
        if self.source[self.position] == "a":
            if (
                self.position + 9 < len(self.source)
                and self.source[self.position : self.position + 9] == "acumulate"
            ):
                self.next = Tkn(Tkn.type.ACUMULATE, "acumulate")
                self.position += 9
                return self.next

        # river
        if self.source[self.position] == "r":
            if (
                self.position + 5 < len(self.source)
                and self.source[self.position : self.position + 5] == "river"
            ):
                self.next = Tkn(Tkn.type.RIVER, "river")
                self.position += 5
                return self.next

        # fish
        if self.source[self.position] == "f":
            if (
                self.position + 4 < len(self.source)
                and self.source[self.position : self.position + 4] == "fish"
            ):
                self.next = Tkn(Tkn.type.FISH, "fish")
                self.position += 4
                return self.next

        # discover
        if self.source[self.position] == "d":
            if (
                self.position + 8 < len(self.source)
                and self.source[self.position : self.position + 8] == "discover"
            ):
                self.next = Tkn(Tkn.type.DISCOVER, "discover")
                self.position += 8
                return self.next

        # sustains
        if self.source[self.position] == "s":
            if (
                self.position + 8 < len(self.source)
                and self.source[self.position : self.position + 8] == "sustains"
            ):
                self.next = Tkn(Tkn.type.SUSTAINS, "sustains")
                self.position += 8
                return self.next

        # event
        if self.source[self.position] == "e":
            if (
                self.position + 5 < len(self.source)
                and self.source[self.position : self.position + 5] == "event"
            ):
                self.next = Tkn(Tkn.type.EVENT, "event")
                self.position += 5
                return self.next

        # conclude
        if self.source[self.position] == "c":
            if (
                self.position + 7 < len(self.source)
                and self.source[self.position : self.position + 8] == "conclude"
            ):
                self.next = Tkn(Tkn.type.CONCLUDE, "conclude")
                self.position += 8
                return self.next

        # rain
        if self.source[self.position] == "r":
            if (
                self.position + 4 < len(self.source)
                and self.source[self.position : self.position + 4] == "rain"
            ):
                self.next = Tkn(Tkn.type.RAIN, "rain")
                self.position += 4
                return self.next

        # dry
        if self.source[self.position] == "d":
            if (
                self.position + 3 < len(self.source)
                and self.source[self.position : self.position + 3] == "dry"
            ):
                self.next = Tkn(Tkn.type.DRY, "dry")
                self.position += 3
                return self.next

        # extinguish
        if self.source[self.position] == "e":
            if (
                self.position + 10 < len(self.source)
                and self.source[self.position : self.position + 10] == "extinguish"
            ):
                self.next = Tkn(Tkn.type.EXTINGUISH, "extinguish")
                self.position += 10
                return self.next

        # pass_time
        if self.source[self.position] == "p":
            if (
                self.position + 8 < len(self.source)
                and self.source[self.position : self.position + 9] == "pass_time"
            ):
                self.next = Tkn(Tkn.type.PASS_TIME, "pass_time")
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
            self.next = Tkn(Tkn.type.IDENTIFIER, self.source[start : self.position])
            return self.next

        # ARROW ->
        if self.source[self.position] == "-" and self.source[self.position + 1] == ">":
            self.next = Tkn(Tkn.type.ARROW, "->")
            self.position += 2
            return self.next

        # FLOW >>
        if self.source[self.position] == ">" and self.source[self.position + 1] == ">":
            self.next = Tkn(Tkn.type.FLOW, ">>")
            self.position += 2
            return self.next

        raise ValueError(
            "Invalid character {character} at position {position}".format(
                position=self.position, character=self.source[self.position]
            )
        )
