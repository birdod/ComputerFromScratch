from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable
from utill import lexical, type, kindmap, opmap, uopmap

class CompilationEngine():
    def __init__(self, filepath, data, static):
        self.writer = VMWriter(filepath)
        self.token = JackTokenizer(data)
        self.table = SymbolTable(static)
        self.token.advance()
        self.CompileClass()
        self.classname = None
        
    def CompileClass(self):
        # 'class'
        self.token.advance() # classname
        self.classname = self.token.keyword()
        self.token.advance() # '{'
        self.token.advance()
        while self.token.symbol() != "}":
            if self.token.keyword() in ["static", "field"]:
                self.CompileClassVarDec()
            elif self.token.keyword() in ["constructor", "function", "method"]:
                self.table.startSubroutine()
                self.CompileSubroutine()
            self.token.advance()
        # '}
        
    def CompileClassVarDec(self):
        # ('static' | 'field')
        kind = self.token.keyword()
        self.token.advance() # type
        type = self.token.keyword()
        self.token.advance() # varName
        name = self.token.keyword()
        self.table.Define(name, type, kind)

        self.token.advance()
        while self.token.symbol() != ";":
            # ','
            self.token.advance() #'varName'
            name = self.token.keyword()
            self.table.Define(name,type,kind)
            self.token.advance()
    
    def CompileSubroutine(self):
        routinekind = self.token.keyword()
        self.token.advance() # rettype
        self.token.advance() # subroutineName
        routinename = self.token.identifier()
        nlocals = 0
        self.token.advance() # '('
        self.token.advance()
        if self.token.symbol() != ')':
            self.compileParameterList()
            self.token.advance()
        self.token.advance() # (subroutineBody) '{'
        self.token.advance()
        while self.token.keyword() == 'var':
            nlocals += self.compileVarDec()
            self.token.advance()
        self.writer.writeFunction(self.classname, routinename, nlocals)
        if routinekind == "constructor":
            fieldcnt = self.table.VarCount("field")
            self.writer.writePush("constant", f"{fieldcnt}")
            self.writer.writeCall("Memory","alloc", "1")
            self.writer.writePop("pointer", "0")
        elif routinekind == "method":
            self.writer.writePush("argument", "0")
            self.writer.writePop("pointer", "0")
        self.compileStatements()
        self.token.advance() # '}'
    
    def compileParameterList(self):
        type = self.token.keyword()
        self.token.advance() #varName
        name = self.token.keyword()
        self.table.Define(name,type,"arg")
        self.token.advance()
        while self.token.symbol() == ',':
            self.token.advance() #
            type = self.token.keyword()
            self.token.advance()
            name = self.token.keyword()
            self.table.Define(name, type, "arg")
            self.token.advance()
        self.token.deadvance()
        return
    
    def compileVarDec(self):
        cnt = 0
        kind = self.token.keyword()
        self.token.advance()
        type = self.token.keyword()
        self.token.advance()
        name = self.token.identifier()
        self.table.Define(name,type, kind)
        cnt += 1
        self.token.advance()
        while self.token.symbol() == ',':
            self.token.advance()
            name = self.token.identifier()
            self.table.Define(name,type, kind)
            cnt += 1
            self.token.advance()
        return cnt
    
    def compileStatements(self):
        while self.token.keyword() in lexical.statement:
            if self.token.keyword() == 'let':
                self.compileLet()
            elif self.token.keyword() == 'if':
                self.compileIf()
            elif self.token.keyword() == 'do':
                self.compileDo()
            elif self.token.keyword() == 'return':
                self.compileReturn()
            elif self.token.keyword() == 'while':
                self.compileWhile()
            self.token.advance()
        self.token.deadvance()
        return
    
    def compileDo(self):
        # do
        classname = None
        self.token.advance() # subroutineName | (className | varName)
        self.token.advance()
        if self.token.symbol() == '(':
            self.token.deadvance()
            subroutineName = self.token.keyword()
            self.token.advance()
        else:
            self.token.deadvance()
            name = self.token.keyword()
            if self.table.KindOf(name) != None:
                location = kindmap[self.table.KindOf(name)]
                self.writer.writePush(location, self.table.IndexOf(name))
                classname = self.table.TypeOf(name)
            else:
                classname = name
            self.token.advance() #'.'
            self.token.advance()
            subroutineName = self.token.keyword()
            self.token.advance()
        self.token.advance() # ')' | expressionList
        nArgs = 0
        if self.token.symbol() != ')':
            nArgs = self.compileExpressionList()
            self.token.advance()
        if classname == None:
            classname = self.classname
        self.writer.writeCall(classname, subroutineName, f"{nArgs}")

        #TODO (is always void call?)
        self.writer.writePop("temp", "0")
        self.token.advance() # ';'
        return
    
    def compileLet(self):
        self.token.advance()
        varName = self.token.identifier()
        varKind = self.table.KindOf(varName)
        varIdx = self.table.IndexOf(varName)
        self.token.advance()
        if self.token.symbol() == '[':
            self.token.advance()
            self.compileExpression()
            self.writer.writePush(f"{kindmap[varKind]}", f"{varIdx}")
            self.writer.WriteArithmetic("add")
            self.token.advance()
            self.token.advance()
            self.token.advance()
            self.compileExpression()
            self.token.advance()
            self.writer.writePop("temp", "0")
            self.writer.writePop("pointer", "1")
            self.writer.writePush("temp","0")
            self.writer.writePop("that", "0")

        else:
            self.token.advance()
            self.compileExpression()
            self.token.advance()
            self.writer.writePop(kindmap[varKind], varIdx)
        return
    
    def compileWhile(self):
        nowcnt = self.table.whilecnt
        self.table.whilecnt += 1
        self.writer.WriteLabel(f"WHILE_EXP{nowcnt}")
        self.token.advance()
        self.token.advance()
        self.compileExpression()
        self.writer.WriteArithmetic("not")
        self.writer.WriteIf(f"WHILE_END{nowcnt}")
        self.token.advance() # )
        self.token.advance() # {
        self.token.advance()
        self.compileStatements()
        self.writer.WriteGoto(f"WHILE_EXP{nowcnt}")
        self.writer.WriteLabel(f"WHILE_END{nowcnt}")
        self.token.advance()
        return
    def compileReturn(self):
        self.token.advance()
        if self.token.symbol() != ';':
            self.compileExpression()
            self.token.advance()
        else:
            self.writer.writePush("constant", "0")
        self.writer.writeReturn()
        return
    def compileIf(self):
        nowcnt = self.table.infcnt
        self.table.infcnt += 1
        self.token.advance()
        self.token.advance()
        self.compileExpression()
        self.writer.WriteIf(f"IF_TRUE{nowcnt}")
        self.writer.WriteGoto(f"IF_FALSE{nowcnt}")
        self.token.advance()
        self.token.advance()
        self.token.advance()
        self.writer.WriteLabel(f"IF_TRUE{nowcnt}")
        self.compileStatements()
        self.writer.WriteGoto(f"IF_END{nowcnt}")
        self.token.advance()
        self.token.advance()
        if self.token.keyword() == 'else':
            self.token.advance()
            self.token.advance()
            self.writer.WriteLabel(f"IF_FALSE{nowcnt}")
            self.compileStatements()
            self.token.advance()
            self.token.advance()
        self.token.deadvance()
        self.writer.WriteLabel(f"IF_END{nowcnt}")
        return
    def compileExpression(self):
        self.compileTerm()
        self.token.advance()
        while self.token.symbol() in lexical.op:
            operation = opmap[self.token.symbol()]
            self.token.advance()
            self.compileTerm()
            self.writer.WriteArithmetic(operation)
            self.token.advance()
        self.token.deadvance()
        return

    def compileTerm(self):
        if self.token.tokenType() == type.INT_CONST:
            self.writer.writePush("constant", f"{self.token.intVal()}")
        elif self.token.tokenType() == type.KEYWORD:
            if self.token.keyword() in ["false", "null"]:
                self.writer.writePush("constant", "0")
            else:
                self.writer.writePush("constant", "0")
                self.writer.WriteArithmetic("not")

        #TODO
        elif self.token.tokenType() == type.STRING_CONST:
            string = self.token.stringVal()
            self.writer.writePush("constant", f"{len(string)+1}")
            self.writer.writeCall("String", "new", "1")
            for element in string:
                self.writer.writePush("constant", f"{ord(element)}")
                self.writer.writeCall("String", "appendChar", "2")
            self.writer.writePush("constant", f"{32}")
            self.writer.writeCall("String", "appendChar", "2")
        elif self.token.symbol() in lexical.uop:
            op = uopmap[self.token.symbol()]
            self.token.advance()
            self.compileTerm()
            self.writer.WriteArithmetic(op)

        elif self.token.symbol() == '(':
            self.token.advance()
            self.compileExpression()
            self.token.advance()

        else:
            self.token.advance()
            #TODO (array index)
            if self.token.symbol() == '[':
                self.token.deadvance()
                varName = self.token.identifier()
                varKind = self.table.KindOf(varName)
                varIdx = self.table.IndexOf(varName)
                self.token.advance()
                self.token.advance()
                self.compileExpression()
                self.writer.writePush(f"{kindmap[varKind]}", f"{varIdx}")

                self.writer.WriteArithmetic("add")
                self.writer.writePop("pointer", "1")
                self.writer.writePush("that", "0")
                self.token.advance()
            elif self.token.symbol() in ['(','.']:
                className = None
                self.token.deadvance()
                self.token.advance()
                if self.token.symbol() == '(':
                    self.token.deadvance()
                    subroutineName = self.token.identifier()
                    self.token.advance()
                else:
                    self.token.deadvance()
                    className = self.token.identifier()
                    self.token.advance()
                    self.token.advance()
                    subroutineName = self.token.identifier()
                    self.token.advance()
                self.token.advance()
                cnt = 0
                if self.token.symbol() != ')':
                    cnt = self.compileExpressionList()
                    self.token.advance()
                if className == None:
                    className = self.classname
                self.writer.writeCall(className, subroutineName, f"{cnt}")
            else:
                self.token.deadvance()
                varName = (self.token.identifier())
                varKind = self.table.KindOf(varName)
                varIdx = self.table.IndexOf(varName)
                self.writer.writePush(kindmap[varKind], varIdx)

        return

    def compileExpressionList(self):
        cnt = 0
        self.compileExpression()
        cnt += 1
        self.token.advance()
        while self.token.symbol() == ',':
            self.token.advance()
            self.compileExpression()
            cnt += 1
            self.token.advance()
        self.token.deadvance()

        return cnt
