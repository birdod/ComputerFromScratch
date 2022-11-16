import utill

class CodeWriter():
    def __init__(self):
        self.file = None
        self.ifcnt = 0
        self.callcnt = 0
        self.current_file = None

    def setFileName(self, filename):
        self.file = open(filename, "w")
    
    def writeInit(self):
        self.file.write("""
        @256
        D=A
        @SP
        M=D
        """)
        self.file.write(utill.call_command(0,'Sys.init', 0))
        self.callcnt += 1

    def writeArithmetic(self, command):
        self.file.write(
            utill.arithmetic_cmdtoasm(self.ifcnt, command)
            )
        self.ifcnt += 1

    def writePushPop(self, command, segment, index):
        self.file.write(
            utill.pushpop_cmdtoasm(self.current_file, command, segment, index)
            )
    
    def writeLabel(self, label):
        self.file.write(
            utill.label_cmdtoasm(self.current_file, label)
        )

    def writeGoto(self, label):
        self.file.write(
            utill.goto_command(self.current_file, label)
        )

    def writeIf(self, label):
        self.file.write(
            utill.if_command(self.current_file, label)
        )

    def writeCall(self, functionName, numArgs):
        self.file.write(
            utill.call_command(self.callcnt,functionName, int(numArgs))
        )
        self.callcnt += 1
    
    def writeReturn(self):
        self.file.write(
            utill.return_command()
        )

    def writeFunction(self, functionName, numLocals):
        self.file.write(
            utill.function_command(functionName, int(numLocals))
        )

    def close(self):
        self.file.close()
