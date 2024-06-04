from abc import ABC, abstractmethod
from symbolTable import Symbol_Table

class Node(ABC):

    def __init__(self, value: int):
        self.value = value
        self.children = []

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
        

class Identifier(Node):
    
        def __init__(self, value: str, st: Symbol_Table):
            super().__init__(value)
            self.st = st
    
        def evaluate(self):
            if self.st.lookup(self.value) == None:
                raise Exception('Variable ' + self.value + ' not found')
            return self.st.lookup(self.value)
    
        def __str__(self):
            return self.value
        
class Create(Node):
    
        def __init__(self, name: str, value1: int, value2: int, st: Symbol_Table, var_type: str):
            super().__init__(value1)
            self.name = name
            self.value1 = value1
            self.value2 = value2
            self.st = st
            self.var_type = var_type


        def evaluate(self):
            self.st.create_assign(self.name, self.value1, self.value2, self.var_type)

        def __str__(self):
            return self.var_type + ' ' + self.name + ' create ' + str(self.value1) + ',' + str(self.value2)
        
class Discover(Node):
    
        def __init__(self, value: int):
            super().__init__(value)

        def evaluate(self):
            value1, value2, type, name = self.value.evaluate()
            if type == 'river':
                print(f'{name} is a river with flow of {value1}')
            elif type == 'fish':
                print(f'{name} is a fish with {value1} population and {value2} of consumption')
            else:
                raise Exception('Invalid operation')

        def __str__(self):
            return 'Discover(' + str(self.value) + ')'
        
class Flow(Node):
    # x >> 5 >> y 
    # a variável x transfere 5 para a variável y
    def __init__(self, value: int, left: Node, right: Node, st: Symbol_Table):
        super().__init__(value)
        self.left = left
        self.right = right
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        varr1, varr2, typer, namer = self.right.evaluate()
        if typel != typer or typel != 'river':
            raise Exception('Invalid operation')
        varl1 = varl1 - self.value
        varr1 = varr1 + self.value
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)
        self.st.insert(namer, varr1, varr2, typer)

    def __str__(self):
        return str(self.left) + ' >> ' + str(self.value) + ' >> ' + str(self.right)
    

class Branch(Node):
    # x branch 5
    # a variável x se ramifica em 5 (x/5)
    def __init__(self, value: int, left: Node, st: Symbol_Table):
        super().__init__(value)
        self.left = left
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        if typel != 'river':
            raise Exception('Invalid operation')
        varl1 = varl1 / self.value
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)

    def __str__(self):
        return str(self.left) + ' branch ' + str(self.value)
    
class Acumulate(Node):
    # x acumulate 5
    # a variável x acumula 5 (x*5)
    def __init__(self, value: int, left: Node, st: Symbol_Table):
        super().__init__(value)
        self.left = left
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        if typel != 'river':
            raise Exception('Invalid operation')
        varl1 = varl1 * self.value
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)

    def __str__(self):
        return str(self.left) + ' acumulate ' + str(self.value)
    

class Arrow(Node):
    # x -> y
    # cada f caça z para aumentar seu numero em (população-população%2)
    def __init__(self, left: Node, right: Node, st: Symbol_Table):
        super().__init__(None)
        self.left = left
        self.right = right
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        varr1, varr2, typer, namer = self.right.evaluate()
        if typel != 'fish':
            raise Exception('Invalid operation')
        sub = varr1 - (varl2*varl1)
        if sub > 0:
            sub = 0
        varr1 = varr1 - (varl2*varl1) # cada z consome x no valor de seu consumo varl2
        varl1 = varl1 + (varl1 - varl1%2) + sub # aumenta seu numero em (população-população%2)
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)
        self.st.insert(namer, varr1, varr2, typer)


    def __str__(self):
        return str(self.left) + ' -> ' + str(self.right)
    

class Sustains(Node):
# x sustains z: # enquanto x sustentar z # para sustentar x é maior que 0 e  cada z consome x no valor de seu consumo varl2
# e aumenta seu numero em (população-população%2) (populaçãox = populaçãox + (populaçãox-populaçãox%2) )

    def __init__(self, child: list, left: Node, right: Node, st: Symbol_Table):
        super().__init__(None)
        self.left = left
        self.right = right
        self.st = st
        self.child = child

    def evaluate(self):
        while self.left.evaluate()[0] > 0:
            varl1, varl2, typel, namel = self.left.evaluate()
            varr1, varr2, typer, namer = self.right.evaluate()
            if typer != 'fish':
                raise Exception('Invalid operation')
            sub = varl1 - (varr2*varr1)
            if sub > 0:
                sub = 0
            varl1 = varl1 - (varr2*varr1)
            varr1 = varr1 + (varr1 - varr1%2) + sub
            # insert the new values in the symbol table
            self.st.insert(namel, varl1, varl2, typel)
            self.st.insert(namer, varr1, varr2, typer)
            for i in self.child:
                i.evaluate()

    def __str__(self):
        return str(self.left) + ' sustains ' + str(self.right)
    

class Event(Node):
    # simple if statement
    # event condition
    def __init__(self, child: list, condition: Node, st: Symbol_Table):
        super().__init__(None)
        self.condition = condition
        self.st = st
        self.child = child

    def evaluate(self):
        if self.condition.evaluate():
            for i in self.child:
                i.evaluate()

    def __str__(self):
        return 'Event(' + str(self.condition) + ')'
    
class Rain(Node):
    def __init__(self, value: Node, st: Symbol_Table):
        super().__init__(None)
        self.value = value
        self.st = st

    def evaluate(self):
        self.val1, val2, type, name = self.value.evaluate()
        if type != 'river':
            raise Exception('Invalid operation')
        all_rivers = self.st.look_all_rivers()
        for i in all_rivers:
            flow = i[0]
            flow += self.val1
            self.st.insert(i[3], flow, i[1], i[2])

    def __str__(self):
        return 'Rain(' + str(self.value) + ')'
    
class Dry(Node):
    def __init__(self, value: Node, st: Symbol_Table):
        super().__init__(None)
        self.value = value
        self.st = st

    def evaluate(self):
        self.val1, val2, type, name = self.value.evaluate()
        if type != 'river':
            raise Exception('Invalid operation')
        all_rivers = self.st.look_all_rivers()
        for i in all_rivers:
            flow = i[0]
            flow -= self.val1
            self.st.insert(i[3], flow, i[1], i[2])

    def __str__(self):
        return 'Dry(' + str(self.value) + ')'
    

class NoOp(Node):
    def __init__(self):
        super().__init__(None)

    def evaluate(self):
        return None

    def __str__(self):
        return 'NoOp()'
    

class Statement(Node):
        
            def __init__(self, value: Node, child: Node):
                super().__init__(value)
                self.child = child
        
            def evaluate(self):
                self.value.evaluate()
                self.child.evaluate()
        
            def __str__(self):
                return f'{self.value} {self.child}'
            

class COMPARISSON(Node):
    def __init__(self, left: Node, right: Node, value: str):
        super().__init__(value)
        self.left = left
        self.right = right

    def evaluate(self):
        if self.value == 'inf':
            return self.left.evaluate() < self.right.evaluate()
        elif self.value == 'sup':
            return self.left.evaluate() > self.right.evaluate()
        elif self.value == 'ig':
            return self.left.evaluate() == self.right.evaluate()

    def __str__(self):
        return f'{self.left} {self.value} {self.right}'
    

class Extinguish(Node):
    def __init__(self, name: str, st: Symbol_Table):
        super().__init__(None)
        self.name = name
        self.st = st

    def evaluate(self):
        self.st.remove(self.name)

    def __str__(self):
        return 'Extinguish(' + self.name + ')'
    







                        

                

                
            
# test
#node = BinOp('+', IntVal(2), BinOp('*', IntVal(3), IntVal(4)))
#print(node.evaluate())
#print(node)
#node = UnOp('-', IntVal(2))
#print(node.evaluate())
#print(node)
#node = NoOp()
#print(node.evaluate())
#print(node)
# Output:
# 14
# (2 + (3 * 4))
# -2
# (-2)
# None
#
