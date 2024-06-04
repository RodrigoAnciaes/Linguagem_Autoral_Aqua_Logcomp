# Tokenizer class
import enum
from tkn import Tkn


class Tknizer(object):
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
        if len(self.source) == 0:
            raise Exception('source cannot be None')
    
    def select_next(self):
        if self.position >= len(self.source):
            next = Tkn(Tkn.type.EOF, None)
            self.next = next
            return next
        
        while self.source[self.position] in [' ','\t', '\r']:
            self.position += 1
            if self.position >= len(self.source):
                next = Tkn(Tkn.type.EOF, None)
                self.next = next
                return next
            
        #\n
        if self.source[self.position] == '\n':
            next = Tkn(Tkn.type.NEWLINE, '\n')
            self.position += 1
            self.next = next
            return next
            
        
        #NUMBER
        if self.source[self.position].isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            next = Tkn(Tkn.type.NUMBER, int(self.source[start:self.position]))
            self.next = next
            return next
        
        #COMMA
        if self.source[self.position] == ',':
            tkn = Tkn(Tkn.type.COMMA, ',')
            self.position += 1
            next = tkn
            self.next = next
            return tkn
        
        #PAREN_OPEN
        if self.source[self.position] == '(':
            tkn = Tkn(Tkn.type.PAREN_OPEN, '(')
            self.position += 1
            next = tkn
            self.next = next
            return tkn
        
        #PAREN_CLOSE
        if self.source[self.position] == ')':
            tkn = Tkn(Tkn.type.PAREN_CLOSE, ')')
            self.position += 1
            next = tkn
            self.next = next
            return tkn
        
        
        ## RESERVED WORDS SECTION ##

        #COMPARISSON (inf, sup, ig)

        #inf ( a inf b)
        if self.source[self.position] == 'i':
            if self.position+3 < len(self.source) and self.source[self.position:self.position+3] == 'inf':
                tkn = Tkn(Tkn.type.COMPARISSON, 'inf')
                self.position += 3
                next = tkn
                self.next = next
                return tkn
            
        #sup ( a sup b)
        if self.source[self.position] == 's':
            if self.position+3 < len(self.source) and self.source[self.position:self.position+3] == 'sup':
                tkn = Tkn(Tkn.type.COMPARISSON, 'sup')
                self.position += 3
                next = tkn
                self.next = next
                return tkn
            
        #ig ( a ig b)
        if self.source[self.position] == 'i':
            if self.position+2 < len(self.source) and self.source[self.position:self.position+2] == 'ig':
                tkn = Tkn(Tkn.type.COMPARISSON, 'ig')
                self.position += 2
                next = tkn
                self.next = next
                return tkn
            

        #create
        if self.source[self.position] == 'c':
            if self.position+6 < len(self.source) and self.source[self.position:self.position+6] == 'create':
                tkn = Tkn(Tkn.type.CREATE, 'create')
                self.position += 6
                next = tkn
                self.next = next
                return tkn
            
        #branch
        if self.source[self.position] == 'b':
            if self.position+6 < len(self.source) and self.source[self.position:self.position+6] == 'branch':
                tkn = Tkn(Tkn.type.BRANCH, 'branch')
                self.position += 6
                next = tkn
                self.next = next
                return tkn
            
        #acumulate
        if self.source[self.position] == 'a':
            if self.position+9 < len(self.source) and self.source[self.position:self.position+9] == 'acumulate':
                tkn = Tkn(Tkn.type.ACUMULATE, 'acumulate')
                self.position += 9
                next = tkn
                self.next = next
                return tkn
            
        #river
        if self.source[self.position] == 'r':
            if self.position+5 < len(self.source) and self.source[self.position:self.position+5] == 'river':
                tkn = Tkn(Tkn.type.RIVER, 'river')
                self.position += 5
                next = tkn
                self.next = next
                return tkn
            
        #fish
        if self.source[self.position] == 'f':
            if self.position+4 < len(self.source) and self.source[self.position:self.position+4] == 'fish':
                tkn = Tkn(Tkn.type.FISH, 'fish')
                self.position += 4
                next = tkn
                self.next = next
                return tkn
            
        #discover
        if self.source[self.position] == 'd':
            if self.position+8 < len(self.source) and self.source[self.position:self.position+8] == 'discover':
                tkn = Tkn(Tkn.type.DISCOVER, 'discover')
                self.position += 8
                next = tkn
                self.next = next
                return tkn
            
        #sustains
        if self.source[self.position] == 's':
            if self.position+8 < len(self.source) and self.source[self.position:self.position+8] == 'sustains':
                tkn = Tkn(Tkn.type.SUSTAINS, 'sustains')
                self.position += 8
                next = tkn
                self.next = next
                return tkn
            
        #event
        if self.source[self.position] == 'e':
            if self.position+5 < len(self.source) and self.source[self.position:self.position+5] == 'event':
                tkn = Tkn(Tkn.type.EVENT, 'event')
                self.position += 5
                next = tkn
                self.next = next
                return tkn
            
        #conclude
        if self.source[self.position] == 'c':
            if self.position+7 < len(self.source) and self.source[self.position:self.position+8] == 'conclude':
                tkn = Tkn(Tkn.type.CONCLUDE, 'conclude')
                self.position += 8
                next = tkn
                self.next = next
                return tkn
            
        #rain
        if self.source[self.position] == 'r':
            if self.position+4 < len(self.source) and self.source[self.position:self.position+4] == 'rain':
                tkn = Tkn(Tkn.type.RAIN, 'rain')
                self.position += 4
                next = tkn
                self.next = next
                return tkn
            
        #dry
        if self.source[self.position] == 'd':
            if self.position+3 < len(self.source) and self.source[self.position:self.position+3] == 'dry':
                tkn = Tkn(Tkn.type.DRY, 'dry')
                self.position += 3
                next = tkn
                self.next = next
                return tkn
            
        #extinguish
        if self.source[self.position] == 'e':
            if self.position+10 < len(self.source) and self.source[self.position:self.position+10] == 'extinguish':
                tkn = Tkn(Tkn.type.EXTINGUISH, 'extinguish')
                self.position += 10
                next = tkn
                self.next = next
                return tkn
            
        #pass_time
        if self.source[self.position] == 'p':
            if self.position+8 < len(self.source) and self.source[self.position:self.position+9] == 'pass_time':
                tkn = Tkn(Tkn.type.PASS_TIME, 'pass_time')
                self.position += 9
                next = tkn
                self.next = next
                return tkn
            

            
            
        
        ## END OF RESERVED WORDS SECTION ##  
            
        #ID
        if self.source[self.position].isalpha():
            start = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            next = Tkn(Tkn.type.IDENTIFIER, self.source[start:self.position])
            self.next = next
            return next
        
        #ARROW ->
        if self.source[self.position] == '-' and self.source[self.position+1] == '>':
            tkn = Tkn(Tkn.type.ARROW, '->')
            self.position += 2
            next = tkn
            self.next = next
            return tkn
        
        #FLOW >>
        if self.source[self.position] == '>' and self.source[self.position+1] == '>':
            tkn = Tkn(Tkn.type.FLOW, '>>')
            self.position += 2
            next = tkn
            self.next = next
            return tkn
        

        
        raise Exception('Invalid character {character} at position {position}'.format(position=self.position, character=self.source[self.position]))