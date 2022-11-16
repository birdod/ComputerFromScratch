

class SymbolTable():
    def __init__(self, static):
        self.general = {}
        self.local = {}
        self.method = {}
        self.arg = 0
        self.var = 0
        self.static = static
        self.field = 0
        self.infcnt = 0
        self.whilecnt = 0
    def startSubroutine(self):
        self.local = {}
        self.arg = 0
        self.var = 0
        self.infcnt = 0
        self.whilecnt = 0
    
    def Define(self, name, type, kind):
        if kind == "static":
            self.general[name] = {"type":type, "kind": kind, "#": self.static}
            self.static += 1
        if kind == "field":
            self.general[name] = {"type":type, "kind": kind, "#": self.field}
            self.field += 1
        if kind == "arg":
            self.local[name] = {"type":type, "kind": kind, "#": self.arg}
            self.arg += 1
        if kind == "var":
            self.local[name] = {"type":type, "kind": kind, "#": self.var}
            self.var += 1

    def VarCount(self, kind):
        if kind == "static":
            return self.static
        elif kind == "field":
            return self.field
        elif kind == "arg":
            return self.arg
        elif kind == "var":
            return self.var

    def KindOf(self, name):
        if name in self.local.keys():
            return self.local[name]["kind"]
        elif name in self.general.keys():
            return self.general[name]["kind"]
        else:
            return None
    def TypeOf(self, name):
        if name in self.local.keys():
            return self.local[name]["type"]
        elif name in self.general.keys():
            return self.general[name]["type"]
        else:
            return None
    def IndexOf(self, name):
        if name in self.local.keys():
            return self.local[name]["#"]
        elif name in self.general.keys():
            return self.general[name]["#"]
        else:
            return None