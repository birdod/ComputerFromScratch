A_COMMAND=123
C_COMMAND=323
L_COMMAND=125

from preprocess import clear


class Parser():
    def __init__(self, path):
        with open(path, 'r') as file:
            data = file.read()
        self.lines = clear(data)
        self.i = 0
        self.now = None

    def hasMoreCommands(self):
        return not (self.i==len(self.lines))
    
    def advance(self):
        self.now = self.lines[self.i]
        self.i += 1
    
    def commandType(self):
        discriminator = self.now[0]
        if discriminator=='@':
            return A_COMMAND
        
        if discriminator=='(':
            return L_COMMAND

        else:
            return C_COMMAND
        
    def symbol(self):
        return f'{int(self.now[1:]):016b}'
    
    def dest(self):
        idx = self.now.find('=')
        if idx==-1:
            return 'null0'
        return self.now[:idx]
    
    def comp(self):
        eqidx = self.now.find('=')
        idx = self.now.find(';')
        if idx==-1:
            return self.now[eqidx+1:]
        else:
            return self.now[eqidx+1:idx]
    
    def jump(self):
        idx = self.now.find(';')
        if idx==-1:
            return 'null'
        return self.now[idx+1:]


class Code():
    def dest(self, string):
        dmap={'null0':'000', 'M':'001', 'D':'010','MD':'011',
        'A':'100','AM':'101','AD':'110','AMD':'111'}
        return dmap[string]
    
    def comp(self, string):
        cmap={'0':'0101010','1':'0111111','-1':'0111010','D':'0001100',
        'A':'0110000', '!D':'0001101','!A':'0110001','-D':'0001111','-A':'0110011',
        'D+1':'0011111','A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010',
        'D-A':'0010011','A-D':'0000111','D&A':'0000000','D|A':'0010101',
        'M':'1110000','!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010',
        'D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000','D|M':'1010101'}
        return cmap[string]
    
    def jump(self, string):
        jmap={'null':'000', 'JGT':'001','JEQ':'010','JGE':'011','JLT':'100',
        'JNE':'101','JLE':'110','JMP':'111'}
        return jmap[string]



if __name__ == '__main__':
    import argparse
    path = argparse.ArgumentParser()
    path.add_argument('filename')
    args = path.parse_args()
    parser = Parser(args.filename)
    code = Code()
    with open(args.filename[:-3] + 'hack', 'w') as f:
        while(parser.hasMoreCommands()):
            parser.advance()
            if parser.commandType()==C_COMMAND:
                f.write('111' +
                code.comp(parser.comp()) +
                code.dest(parser.dest()) + 
                code.jump(parser.jump()) + '\n')
            elif parser.commandType()==L_COMMAND:
                continue
            else:
                f.write(parser.symbol() + '\n')