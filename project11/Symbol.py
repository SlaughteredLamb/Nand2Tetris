class table:
    #Creates a new empty symbol table.
    def __init__(self):
        self.classScope = {}
        self.subroutineScope = {}
        self.currentScope=self.classScope
        self.static = 0
        self.field = 0
        self.arg = 0
        self.var = 0
        self.If = 0
        self.While = 0

    #Starts a new subroutine scope (i.e., resets the subroutine¡¯s symbol table).
    def startSubroutine(self,name):
        self.subroutineScope[name]={}
        self.arg = 0
        self.var = 0
        self.If = 0
        self.While = 0

    #De?nes a new identi?er of a given name, type, and kind and assigns it a running index. STATIC and FIELD identi?ers
    # have a class scope, while ARG and VAR identi?ers have a subroutine scope.
    def define(self, name, type, kind):
        if kind == "static":
            self.classScope[name] = (type, kind, self.static)
            self.static += 1
        elif kind == "field":
            self.classScope[name] = (type, kind, self.field)
            self.field += 1
        elif kind == 'arg':
            self.currentScope[name] = (type, kind, self.arg)
            self.arg += 1
        elif kind == 'var':
            self.currentScope[name] = (type, kind, self.var)
            self.var += 1

    #Returns the number of variables of the given kind already de?ned in the current scope.
    def varCount(self, kind):
        return len([v for (k, v) in self.currentScope.items() if v[1] == kind])

    #Returns the kind of the named identi?er in the current scope. If the identi?er is unknown in the current scope,
    # returns NONE
    def kindOf(self, name):
        if name in self.currentScope:
            return self.currentScope[name][1]
        elif name in self.classScope:
            return self.classScope[name][1]
        else:
            return "NONE"

    #Returns the type of the named identi?er in the current scope.
    def typeOf(self, name):
        if name in self.currentScope:
            return self.currentScope[name][0]
        elif name in self.classScope:
            return self.classScope[name][0]
        else:
            return "NONE"

    #Returns the index assigned to the named identi?er.
    def indexOf(self, name):
        if name in self.currentScope:
            return self.currentScope[name][2]
        elif name in self.classScope:
            return self.classScope[name][2]
        else:
            return "NONE"

    # Returns the number of variables of the given kind already de?ned in the class scope without using scopeChange().
    def classCount(self, kind):
        return len([v for (k, v) in self.classScope.items() if v[1] == kind])

    # Change current scope between two kinds of scope.
    def scopeChange(self, name):
        if name != 0:
            self.currentScope = self.subroutineScope[name]
        else:
            self.currentScope = self.classScope