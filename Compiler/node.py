
"""
This module contains the implementation of various nodes 
used in the compiler's abstract syntax tree (AST).
Classes:
- Node: Abstract base class representing a node in a tree structure.
- Identifier: Represents an identifier node in the abstract syntax tree.
- Create: Represents a create operation.
- Discover: Represents a Discover node in the abstract syntax tree.
- Flow: Represents a flow node in the compiler.
- Branch: Represents a branch node in the compiler.
- Acumulate: Represents a node that performs accumulation operation on a variable.
- Arrow: Represents an Arrow node in the abstract syntax tree (AST).
- Sustains: Represents a sustains operation in the compiler.
- Event: Represents an event node in the compiler.
- Rain: Initializes a Rain object.
- Dry: Initializes a Dry node.
- NoOp: Represents a NoOp node in the abstract syntax tree (AST).
- Statement: Represents a statement node in the compiler.
- COMPARISSON: Initializes a COMPARISSON object.
- Extinguish: Represents a node in the compiler's abstract syntax tree (AST) 
that removes a variable from the symbol table.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from abc import ABC, abstractmethod
from Compiler.symbol_table import SymbolTable


class Node(ABC):
    """
    Abstract base class representing a node in a tree structure.
    Attributes:
        value (int): The value associated with the node.
        children (list): The list of child nodes.
    Methods:
        evaluate(): Abstract method to evaluate the node.
        __str__(): Abstract method to return a string representation of the node.
    """

    def __init__(self, value: int):
        self.value = value
        self.children = []

    @abstractmethod
    def evaluate(self):
        """
        Abstract method to evaluate the node.
        This method should be implemented by subclasses to define the evaluation logic.
        """

    @abstractmethod
    def __str__(self):
        pass


class Identifier(Node):
    """
    Represents an identifier node in the abstract syntax tree.
    Args:
        value (str): The value of the identifier.
        st (SymbolTable): The symbol table associated with the identifier.
    Attributes:
        value (str): The value of the identifier.
        st (SymbolTable): The symbol table associated with the identifier.
    Methods:
        evaluate(): Evaluates the identifier by looking up its value in the symbol table.
    """

    def __init__(self, value: str, st: SymbolTable):
        super().__init__(value)
        self.st = st

    def evaluate(self):
        if self.st.lookup(self.value) is None:
            raise ValueError("Variable " + self.value + " not found")
        return self.st.lookup(self.value)

    def __str__(self):
        return self.value


class Create(Node):
    """
    Represents a create operation.
    Args:
        name (str): The name of the variable being created.
        value1 (int): The first value used in the create operation.
        value2 (int): The second value used in the create operation.
        st (SymbolTable): The symbol table used for variable management.
        var_type (str): The type of the variable being created.
    Attributes:
        name (str): The name of the variable being created.
        value1 (int): The first value used in the create operation.
        value2 (int): The second value used in the create operation.
        st (SymbolTable): The symbol table used for variable management.
        var_type (str): The type of the variable being created.
    Methods:
        evaluate(): Performs the create operation 
        and assigns the result to the variable in the symbol table.
    Returns:
        None
    Raises:
        None
    Usage:
        create_node = Create(name, value1, value2, st, var_type)
        create_node.evaluate()
    """

    def __init__(
        self, name: str, value1: int, value2: int, st: SymbolTable, var_type: str
    ):
        super().__init__(value1)
        self.name = name
        self.value1 = value1
        self.value2 = value2
        self.st = st
        self.var_type = var_type

    def evaluate(self):
        self.st.create_assign(self.name, self.value1, self.value2, self.var_type)

    def __str__(self):
        return (
            self.var_type
            + " "
            + self.name
            + " create "
            + str(self.value1)
            + ","
            + str(self.value2)
        )


class Discover(Node):
    """
    Represents a Discover node in the abstract syntax tree.
    Args:
        value (int): The value of the node.
    Attributes:
        value (int): The value of the node.
    Methods:
        evaluate(): Evaluates the node and prints information based on the type of the value.
    """

    def evaluate(self):
        value1, value2, type_, name = self.value.evaluate()
        if type_ == "river":
            print(f"{name} is a river with flow of {value1}")
        elif type_ == "fish":
            print(
                f"{name} is a fish with {value1} population and {value2} of consumption"
            )
        else:
            raise ValueError("Invalid operation")

    def __str__(self):
        return f"Discover({str(self.value)})"


class Flow(Node):
    """
    Represents a flow node in the compiler.
    Args:
        value (int): The value to be transferred.
        left (Node): The left node.
        right (Node): The right node.
        st (SymbolTable): The symbol table.
    Attributes:
        left (Node): The left node.
        right (Node): The right node.
        st (SymbolTable): The symbol table.
    Methods:
        evaluate: Evaluates the flow node.
    """

    # x >> 5 >> y
    # a variável x transfere 5 para a variável y
    def __init__(self, value: int, left: Node, right: Node, st: SymbolTable):
        super().__init__(value)
        self.left = left
        self.right = right
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        varr1, varr2, typer, namer = self.right.evaluate()
        if typel != typer or typel != "river":
            raise ValueError("Invalid operation")
        varl1 = varl1 - self.value
        varr1 = varr1 + self.value
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)
        self.st.insert(namer, varr1, varr2, typer)

    def __str__(self):
        return str(self.left) + " >> " + str(self.value) + " >> " + str(self.right)


class Branch(Node):
    """
    Represents a branch node in the compiler.
    Args:
        value (int): The value of the branch.
        left (Node): The left child node.
        st (SymbolTable): The symbol table.
    Attributes:
        left (Node): The left child node.
        st (SymbolTable): The symbol table.
    Methods:
        evaluate(): Evaluates the branch node.
    """

    # x branch 5
    # a variável x se ramifica em 5 (x/5)
    def __init__(self, value: int, left: Node, st: SymbolTable):
        super().__init__(value)
        self.left = left
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        if typel != "river":
            raise ValueError("Invalid operation")
        varl1 = varl1 / self.value
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)

    def __str__(self):
        return str(self.left) + " branch " + str(self.value)


class Acumulate(Node):
    """
    Represents a node that performs accumulation operation on a variable.
    Args:
        value (int): The value to be multiplied with the variable.
        left (Node): The left child node.
        st (SymbolTable): The symbol table.
    Attributes:
        value (int): The value to be multiplied with the variable.
        left (Node): The left child node.
        st (SymbolTable): The symbol table.
    Methods:
        evaluate(): Evaluates the accumulation operation and updates the symbol table.
        __str__(): Returns a string representation of the node.
    Raises:
        ValueError: If the type of the variable is not "river".
    """

    # x acumulate 5
    # a variável x acumula 5 (x*5)
    def __init__(self, value: int, left: Node, st: SymbolTable):
        super().__init__(value)
        self.left = left
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        if typel != "river":
            raise ValueError("Invalid operation")
        varl1 = varl1 * self.value
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)

    def __str__(self):
        return str(self.left) + " acumulate " + str(self.value)


class Arrow(Node):
    """
    Represents an Arrow node in the abstract syntax tree (AST).
    Args:
        left (Node): The left child node.
        right (Node): The right child node.
        st (SymbolTable): The symbol table.
    Attributes:
        left (Node): The left child node.
        right (Node): The right child node.
        st (SymbolTable): The symbol table.
    Methods:
        evaluate(): Evaluates the Arrow node.
    Raises:
        ValueError: If the left child node's type is not "fish".
    Returns:
        None
    """

    # x -> y
    # cada f caça z para aumentar seu numero em (população-população%2)
    def __init__(self, left: Node, right: Node, st: SymbolTable):
        super().__init__(None)
        self.left = left
        self.right = right
        self.st = st

    def evaluate(self):
        varl1, varl2, typel, namel = self.left.evaluate()
        varr1, varr2, typer, namer = self.right.evaluate()
        if typel != "fish":
            raise ValueError("Invalid operation")
        sub = varr1 - (varl2 * varl1)
        sub = min(sub, 0)
        varr1 = varr1 - (
            varl2 * varl1
        )  # cada z consome x no valor de seu consumo varl2
        varl1 = (
            varl1 + (varl1 - varl1 % 2) + sub
        )  # aumenta seu numero em (população-população%2)
        # insert the new values in the symbol table
        self.st.insert(namel, varl1, varl2, typel)
        self.st.insert(namer, varr1, varr2, typer)

    def __str__(self):
        return str(self.left) + " -> " + str(self.right)


class Sustains(Node):
    """
    Represents a sustains operation in the compiler.
    Args:
        child (list): List of child nodes.
        left (Node): Left node.
        right (Node): Right node.
        st (SymbolTable): Symbol table.
    Attributes:
        left (Node): Left node.
        right (Node): Right node.
        st (SymbolTable): Symbol table.
        child (list): List of child nodes.
    Methods:
        evaluate(): Evaluates the sustains operation.
    """

    # x sustains z: # enquanto x sustentar z
    # para sustentar x é maior que 0 e  cada z consome x no valor de seu consumo varl2
    # e aumenta seu numero em
    # (população-população%2) (populaçãox = populaçãox + (populaçãox-populaçãox%2) )

    def __init__(self, child: list, left: Node, right: Node, st: SymbolTable):
        super().__init__(None)
        self.left = left
        self.right = right
        self.st = st
        self.child = child

    def evaluate(self):
        while self.left.evaluate()[0] > 0:
            varl1, varl2, typel, namel = self.left.evaluate()
            varr1, varr2, typer, namer = self.right.evaluate()
            if typer != "fish":
                raise ValueError("Invalid operation")
            sub = varl1 - (varr2 * varr1)
            sub = min(sub, 0)
            varl1 = varl1 - (varr2 * varr1)
            varr1 = varr1 + (varr1 - varr1 % 2) + sub
            # insert the new values in the symbol table
            self.st.insert(namel, varl1, varl2, typel)
            self.st.insert(namer, varr1, varr2, typer)
            for i in self.child:
                i.evaluate()

    def __str__(self):
        return str(self.left) + " sustains " + str(self.right)


class Event(Node):
    """
    Represents an event node in the compiler.
    Args:
        child (list): A list of child nodes.
        condition (Node): The condition node for the event.
        st (SymbolTable): The symbol table for the event.
    Attributes:
        condition (Node): The condition node for the event.
        st (SymbolTable): The symbol table for the event.
        child (list): A list of child nodes.
    Methods:
        evaluate(): Evaluates the event by checking the condition
        and executing the child nodes if the condition is true.
    """

    # simple if statement
    # event condition
    def __init__(self, child: list, condition: Node, st: SymbolTable):
        super().__init__(None)
        self.condition = condition
        self.st = st
        self.child = child

    def evaluate(self):
        if self.condition.evaluate():
            for i in self.child:
                i.evaluate()

    def __str__(self):
        return "Event(" + str(self.condition) + ")"


class Rain(Node):
    """
    Initializes a Rain object.
    Args:
        value (Node): The value of the Rain object.
        st (SymbolTable): The symbol table associated with the Rain object.
    """

    def __init__(self, value: Node, st: SymbolTable):
        super().__init__(None)
        self.value = value
        self.st = st
        self.val1 = None

    def evaluate(self):
        self.val1, _, type_, _ = self.value.evaluate()
        if type_ != "river":
            raise ValueError("Invalid operation")
        all_rivers = self.st.look_all_rivers()
        for i in all_rivers:
            flow = i[0]
            flow += self.val1
            self.st.insert(i[3], flow, i[1], i[2])

    def __str__(self):
        return "Rain(" + str(self.value) + ")"


class Dry(Node):
    """
    Initializes a Dry node.
    Args:
        value (Node): The value node representing the amount of water to remove.
        st (SymbolTable): The symbol table containing the rivers.
    Attributes:
        value (Node): The value node representing the amount of water to remove.
        st (SymbolTable): The symbol table containing the rivers.
        val1 (None): Placeholder for the evaluated value of the 'value' node.
    """

    def __init__(self, value: Node, st: SymbolTable):
        super().__init__(None)
        self.value = value
        self.st = st
        self.val1 = None

    def evaluate(self):
        self.val1, _, type_, _ = self.value.evaluate()
        if type_ != "river":
            raise ValueError("Invalid operation")
        all_rivers = self.st.look_all_rivers()
        for i in all_rivers:
            flow = i[0]
            flow -= self.val1
            self.st.insert(i[3], flow, i[1], i[2])

    def __str__(self):
        return "Dry(" + str(self.value) + ")"


class NoOp(Node):
    """
    Represents a NoOp node in the abstract syntax tree (AST).
    A NoOp node is used to represent an empty statement in the code.
    Attributes:
        None
    Methods:
        evaluate: Evaluates the NoOp node and returns None.
        __str__: Returns a string representation of the NoOp node.
    Example usage:
        >>> node = NoOp()
        >>> node.evaluate()
        None
        >>> str(node)
        'NoOp()'
    """

    def __init__(self):
        super().__init__(None)

    def evaluate(self):
        return None

    def __str__(self):
        return "NoOp()"


class Statement(Node):
    """
    Represents a statement node in the compiler.
    Args:
        value (Node): The value of the statement.
        child (Node): The child node of the statement.
    Attributes:
        value (Node): The value of the statement.
        child (Node): The child node of the statement.
    Methods:
        evaluate(): Evaluates the statement by 
        calling the evaluate method of its value and child nodes.
        __str__(): Returns a string representation of the statement.
    """

    def __init__(self, value: Node, child: Node):
        super().__init__(value)
        self.child = child

    def evaluate(self):
        self.value.evaluate()
        self.child.evaluate()

    def __str__(self):
        return f"{self.value} {self.child}"


class COMPARISSON(Node):
    """
    Initializes a COMPARISSON object.
    Args:
        left (Node): The left operand of the comparison.
        right (Node): The right operand of the comparison.
        value (str): The type of comparison to be performed.
    Attributes:
        left (Node): The left operand of the comparison.
        right (Node): The right operand of the comparison.
        value (str): The type of comparison to be performed.
    """

    def __init__(self, left: Node, right: Node, value: str):
        super().__init__(value)
        self.left = left
        self.right = right

    def evaluate(self):
        if self.value == "inf":
            return self.left.evaluate() < self.right.evaluate()
        if self.value == "sup":
            return self.left.evaluate() > self.right.evaluate()
        if self.value == "ig":
            return self.left.evaluate() == self.right.evaluate()
        raise ValueError("Invalid operation")

    def __str__(self):
        return f"{self.left} {self.value} {self.right}"


class Extinguish(Node):
    """
    Extinguish class represents a node in the compiler's abstract syntax tree (AST) 
    that removes a variable from the symbol table.
    Attributes:
        name (str): The name of the variable to be removed.
        st (SymbolTable): The symbol table from which the variable will be removed.
    Methods:
        evaluate(): Removes the variable from the symbol table.
        __str__(): Returns a string representation of the Extinguish node.
    """

    def __init__(self, name: str, st: SymbolTable):
        super().__init__(None)
        self.name = name
        self.st = st

    def evaluate(self):
        self.st.remove(self.name)

    def __str__(self):
        return "Extinguish(" + self.name + ")"
