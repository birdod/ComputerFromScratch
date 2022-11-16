from utill import pre
C_ARITHMETIC, C_PUSH, C_POP, C_LABEL, \
C_GOTO, C_IF, C_FUNCTION, C_RETURN, C_CALL = [i for i in range(9)]
arithmetic_list = ['add','sub','neg','eq','gt','lt','and','or','not']

class Parser():
    def __init__(self,file):
        self.data = pre(file)
        self.now = None
        self.cnt = 0
    
    def hasMoreCommands(self):
        return not(len(self.data)==self.cnt)

    def advance(self):
        self.now = self.data[self.cnt].split()
        self.cnt += 1
    
    def commandType(self):
        command = self.now[0]
        if command in arithmetic_list:
            return C_ARITHMETIC
        elif command == 'push':
            return C_PUSH
        elif command == 'pop':
            return C_POP
        elif command == 'label':
            return C_LABEL
        elif command == 'goto':
            return C_GOTO
        elif command == 'if-goto':
            return C_IF
        elif command == 'function':
            return C_FUNCTION
        elif command == 'return':
            return C_RETURN
        elif command == 'call':
            return C_CALL
        
    def arg1(self):
        if self.commandType()==C_ARITHMETIC:
            return self.now[0]
        else:
            return self.now[1]
        
    def arg2(self):
        return self.now[2]


