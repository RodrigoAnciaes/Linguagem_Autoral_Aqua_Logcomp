"""
Symbol Table Management System

This module defines the SymbolTable class, which is responsible for managing symbols 
in a table. Each symbol can be associated with values and a type, representing different 
entities (such as rivers and fish) and their respective data.

Classes:
    - SymbolTable: Manages symbols, allowing insertion, lookup, creation, and removal of symbols.

Class Symbol_Table:
    Methods:
        - insert(name, value1, value2, type_):
          Inserts a variable (symbol) into the table with given attributes.
        - lookup(name): Looks up a variable by its name in the symbol table.
        - look_all_rivers(): Returns a list of all symbols representing rivers.
        - look_all_fishes(): Returns a list of all symbols representing fish.
        - create(name): Creates a new symbol without assigning any values.
        - create_assign(name, value1, value2, type_):
          Creates and assigns values to a symbol in the table.
        - remove(name): Removes a symbol from the symbol table by name.

Usage Example:
    table = SymbolTable()
    table.create('Amazon River')
    table.create_assign('Salmon', 1000, 200, 'fish')
    table.insert('Amazon River', 5000, 300, 'river')
    river_data = table.lookup('Amazon River')
    all_fish = table.look_all_fishes()
"""

class SymbolTable:

    """
    Class representing a symbol table.
    Methods:
        - insert(name, value1, value2, type_): Inserts a variable into the symbol table.
        - lookup(name): Looks up a variable in the symbol table.
        - look_all_rivers(): Returns a list of all the rivers in the symbol table.
        - look_all_fishes(): Returns a list of all fish symbols in the symbol table.
        - create(name): Creates a new variable in the symbol table.
        - create_assign(name, value1, value2, type_): Creates an assignment in the symbol table.
        - remove(name): Removes a symbol from the symbol table.
    """

    def __init__(self):
        self.symbols = {}
        self.auto_id = id(self)

    def insert(self, name, value1, value2, type_):
        """
        Inserts a variable into the symbol table.

        Parameters:
            name (str): The name of the variable.
            value1 (int): The first value of the variable.
            value2 (int): The second value of the variable.
            type_ (str): The type of the variable.

        Raises:
            ValueError: If the variable already exists in the symbol table.
            ValueError: If the value2 is negative.
        """
        if name in self.symbols:
            if value2 < 0:
                raise ValueError("Negative value for consumption")
            value1 = max(value1, 0)
            self.symbols[name] = (value1, value2, type_, name)
        else:
            raise ValueError(f"Variable {name} not found in symbol table (insert)")

    def lookup(self, name):
        """
        Looks up a variable in the symbol table.

        Parameters:
        - name (str): The name of the variable to look up.

        Returns:
        - The value associated with the variable.

        Raises:
        - ValueError: If the variable is not found in the symbol table.
        """
        # print(f'Looked up {name} with value {self.symbols.get(name)}')
        if name in self.symbols:
            return self.symbols.get(name)
        raise ValueError(f"Variable {name} not found in symbol table (lookup)")

    def look_all_rivers(self):
        """
        Returns a list of all the rivers in the symbol table.

        Returns:
            list: A list of rivers in the symbol table.
        """
        rivers = []
        for _, value in self.symbols.items():
            if value[2] == "river":
                rivers.append(value)
        return rivers

    def look_all_fishes(self):
        """
        Returns a list of all fish symbols in the symbol table.

        Returns:
            list: A list of fish symbols in the symbol table.
        """
        fishes = []
        for _, value in self.symbols.items():
            if value[2] == "fish":
                fishes.append(value)
        return fishes

    def create(self, name):
        """
        Creates a new variable in the symbol table.

        Parameters:
            name (str): The name of the variable to be created.

        Raises:
            ValueError: If the variable already exists in the symbol table.
        """
        if name in self.symbols:
            raise ValueError(f"Variable {name} already exists")
        self.symbols[name] = None

    def create_assign(self, name, value1, value2, type_):
        """
        Creates an assignment in the symbol table.

        Args:
            name (str): The name of the symbol.
            value1 (int): The value of the first parameter.
            value2 (int): The value of the second parameter.
            type_ (str): The type of the symbol.

        Raises:
            ValueError: If value2 is negative.
            ValueError: If value1 is negative.
        """
        if value2 < 0:
            raise ValueError("Negative value for consumption")
        if value1 < 0:
            raise ValueError("Negative value for population")
        self.symbols[name] = (value1, value2, type_, name)

    def remove(self, name):
        """
        Removes a symbol from the symbol table.

        Parameters:
            name (str): The name of the symbol to be removed.

        Returns:
            None
        """
        if name in self.symbols:
            del self.symbols[name]
