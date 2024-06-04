


class Symbol_Table:
    def __init__(self):
        self.symbols = {}
        self.auto_id = id(self)

    def insert(self, name, value1, value2, type):
        if name in self.symbols:
            self.symbols[name] = (value1, value2, type, name)
        else:
            raise Exception(f'Variable {name} not found in symbol table (insert)')
        


    def lookup(self, name):
        #print(f'Looked up {name} with value {self.symbols.get(name)}')
        if name in self.symbols:
            return self.symbols.get(name)
        else:
            print('teste_sy',self.symbols)
            print('tsy2', self.symbols.keys())
            print('tsy5', name)
            print('tsy6', self.auto_id)
            raise Exception(f'Variable {name} not found in symbol table (lookup)')
        
    def look_all_rivers(self):
        rivers = []
        for key in self.symbols.keys():
            if self.symbols[key][2] == 'river':
                rivers.append(self.symbols[key])
        return rivers
    
    def look_all_fishes(self):
        fishes = []
        for key in self.symbols.keys():
            if self.symbols[key][2] == 'fish':
                fishes.append(self.symbols[key])
        return fishes
    
    def create(self, name):
        if name in self.symbols:
            raise Exception(f'Variable {name} already exists')
        self.symbols[name] = None

    def create_assign(self, name, value1, value2, type):
        #if name in self.symbols:
            #raise Exception(f'Variable {name} already exists')
        #print('teste_ca', self.auto_id)
        self.symbols[name] = (value1, value2, type, name)

    def remove(self, name):
        if name in self.symbols:
            del self.symbols[name]


def main():
    st = Symbol_Table()
    st.insert('a', 1)
    st.insert('b', 2)
    st.insert('c', 3)
    print(st.lookup('a'))
    print(st.lookup('b'))
    print(st.lookup('c'))
    st.remove('b')
    print(st.lookup('b'))


if __name__ == '__main__':
    main()