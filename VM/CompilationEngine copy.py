# # from JackTokenizer import JackTokenizer
# # from VMWriter import VMWriter
# from utill import lexical, type

# class CompilationEngine():
#     def __init__(self, filepath, data):
#         self.writer = VMWriter(filepath)
#         self.token = JackTokenizer(data)
#         self.token.advance()
#         self.CompileClass()

#     def CompileClass(self):
#         self.file.write("<class>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()

#         while self.token.symbol() != "}":
#             if self.token.keyword() in ["static", "field"]:
#                 self.CompileClassVarDec()
#             elif self.token.keyword() in ["constructor", "function", "method"]:
#                 self.CompileSubroutine()
#             self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.file.write("</class>\n")
#         return
        
#     def CompileClassVarDec(self):
#         self.file.write("<classVarDec>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         if self.token.keyword() in lexical.keyword:
#             self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         else:
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         while self.token.symbol() != ";":
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.file.write("</classVarDec>\n")
#         return
    
#     def CompileSubroutine(self):
#         self.file.write("<subroutineDec>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         if self.token.keyword() in lexical.keyword:
#             self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         else:
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         if self.token.symbol() != ')':
#             self.compileParameterList()
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         else:
#             self.file.write("<parameterList>\n")
#             self.file.write("</parameterList>\n")
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.file.write("<subroutineBody>\n")
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         while self.token.keyword() == 'var':
#             self.compileVarDec()
#             self.token.advance()
#         self.compileStatements()
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.file.write("</subroutineBody>\n")

#         self.file.write("</subroutineDec>\n")

#         return
    
#     def compileParameterList(self):
#         self.file.write("<parameterList>\n")
#         if self.token.keyword() in lexical.keyword:
#             self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         else:
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         while self.token.symbol() == ',':
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             if self.token.keyword() in lexical.keyword:
#                 self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#             else:
#                 self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance()
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance()
#         self.token.deadvance()
#         self.file.write("</parameterList>\n")

#         return
    
#     def compileVarDec(self):
#         self.file.write("<varDec>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         if self.token.keyword() in lexical.keyword:
#             self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         else:
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         while self.token.symbol() == ',':
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")

#         self.file.write("</varDec>\n")
#         return
    
#     def compileStatements(self):
#         self.file.write("<statements>\n")
#         while self.token.keyword() in lexical.statement:
#             if self.token.keyword() == 'let':
#                 self.compileLet()
#             elif self.token.keyword() == 'if':
#                 self.compileIf()
#             elif self.token.keyword() == 'do':
#                 self.compileDo()
#             elif self.token.keyword() == 'return':
#                 self.compileReturn()
#             elif self.token.keyword() == 'while':
#                 self.compileWhile()
#             self.token.advance()
#         self.token.deadvance()
#         self.file.write("</statements>\n")

#         return
    
#     def compileDo(self):
#         self.file.write("<doStatement>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()

#         self.token.advance()
#         if self.token.symbol() == '(':
#             self.token.deadvance()
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         else:
#             self.token.deadvance()
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         if self.token.symbol() != ')':
#             self.compileExpressionList()
#             self.token.advance()
#         else:
#             self.file.write("<expressionList>\n")
#             self.file.write("</expressionList>\n")
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")

#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")

#         self.file.write("</doStatement>\n")
#         return
    
#     def compileLet(self):
#         self.file.write("<letStatement>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#         self.token.advance()
#         if self.token.symbol() == '[':
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.compileExpression()
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.compileExpression()
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.file.write("</letStatement>\n")
#         return
    
#     def compileWhile(self):
#         self.file.write("<whileStatement>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.compileExpression()
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.compileStatements()
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.file.write("</whileStatement>\n")

#         return
#     def compileReturn(self):
#         self.file.write("<returnStatement>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         if self.token.symbol() != ';':
#             self.compileExpression()
#             self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.file.write("</returnStatement>\n")
        
#         return
#     def compileIf(self):
#         self.file.write("<ifStatement>\n")
#         self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.compileExpression()
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         self.compileStatements()
#         self.token.advance()
#         self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#         self.token.advance()
#         if self.token.keyword() == 'else':
#             self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.compileStatements()
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#         self.token.deadvance()
#         self.file.write("</ifStatement>\n")

#         return
#     def compileExpression(self):
#         self.file.write("<expression>\n")
#         self.compileTerm()
#         self.token.advance()
#         while self.token.symbol() in lexical.op:
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.compileTerm()
#             self.token.advance()
#         self.token.deadvance()
#         self.file.write("</expression>\n")

#         return
#     def compileTerm(self):
#         self.file.write("<term>\n")
#         if self.token.tokenType() == type.INT_CONST:
#             self.file.write(f"<integerConstant> {self.token.intVal()} </integerConstant>\n")
#         elif self.token.tokenType() == type.KEYWORD:
#             self.file.write(f"<keyword> {self.token.keyword()} </keyword>\n")
#         elif self.token.tokenType() == type.STRING_CONST:
#             self.file.write(f"<stringConstant> {self.token.stringVal()} </stringConstant>\n")
#         elif self.token.symbol() in lexical.uop:
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.compileTerm()
#         elif self.token.symbol() == '(':
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.compileExpression()
#             self.token.advance()
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")

#         else:
#             self.token.advance()
#             if self.token.symbol() == '[':
#                 self.token.deadvance()
#                 self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#                 self.token.advance()
#                 self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#                 self.token.advance()
#                 self.compileExpression()
#                 self.token.advance()
#                 self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             elif self.token.symbol() in ['(','.']:
#                 self.token.deadvance()
#                 self.token.advance()
#                 if self.token.symbol() == '(':
#                     self.token.deadvance()
#                     self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#                     self.token.advance()
#                     self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#                 else:
#                     self.token.deadvance()
#                     self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#                     self.token.advance()
#                     self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#                     self.token.advance()
#                     self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")
#                     self.token.advance()
#                     self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#                 self.token.advance()
#                 if self.token.symbol() != ')':
#                     self.compileExpressionList()
#                     self.token.advance()
#                 else:
#                     self.file.write("<expressionList>\n")
#                     self.file.write("</expressionList>\n")
#                 self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             else:
#                 self.token.deadvance()
#                 self.file.write(f"<identifier> {self.token.identifier()} </identifier>\n")

#         self.file.write("</term>\n")
#         return
#     def compileExpressionList(self):
#         self.file.write("<expressionList>\n")
#         self.compileExpression()
#         self.token.advance()
#         while self.token.symbol() == ',':
#             self.file.write(f"<symbol> {self.token.symbol()} </symbol>\n")
#             self.token.advance()
#             self.compileExpression()
#             self.token.advance()
#         self.token.deadvance()
#         self.file.write("</expressionList>\n")

#         return
