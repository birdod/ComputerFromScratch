

class VMWriter():
    def __init__(self, filepath):
        self.file = open(filepath, "w")
    
    def writePush(self, segment, index):
        self.file.write(f"push {segment} {index}\n")
    
    def writePop(self, segment, index):
        self.file.write(f"pop {segment} {index}\n")
    
    def WriteArithmetic(self, command):
        self.file.write(f"{command}\n")
    
    def WriteLabel(self, label):
        self.file.write(f"label {label}\n")
    
    def WriteGoto(self, label):
        self.file.write(f"goto {label}\n")

    def WriteIf(self, label):
        self.file.write(f"if-goto {label}\n")
    
    def writeCall(self, classname, name, nArgs):
        self.file.write(f"call {classname}.{name} {nArgs}\n")

    def writeFunction(self, classname, name, nLocals):
        self.file.write(f"function {classname}.{name} {nLocals}\n")

    def writeReturn(self):
        self.file.write(f"return\n")

    def Close(self):
        self.file.close()