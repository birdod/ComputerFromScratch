from utill import pre, lexical, type



class JackTokenizer():
    def __init__(self, data):
        self.data = pre(data)
        self.now = None
        self.i = 0
    
    def hasMoreTokens(self):
        return self.i < len(self.data)

    def advance(self):
        self.now = self.data[self.i]
        self.i += 1
    
    def deadvance(self):
        self.now = self.data[self.i-2]
        self.i -= 1
    
    def tokenType(self):
        if self.now in lexical.keyword:
            return type.KEYWORD
        elif self.now in lexical.symbols:
            return type.SYMBOL
        elif self.now[0] == '\"':
            return type.STRING_CONST
        elif self.now[0].isnumeric():
            return type.INT_CONST
        else:
            return type.IDENTIFIER
    
    def keyword(self):
        return self.now

    def symbol(self):
        return self.now
    
    def identifier(self):
        return self.now
    
    def intVal(self):
        return int(self.now)
    
    def stringVal(self):
        return self.now[1:-1]