import sys
import os
import Tokenizer
import Symbol


def Constructor(iname, outname):
    keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int',
               'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
    f = open(iname, 'r')
    fOut = []
    mark = 0
    for line in f:
        e = ''
        if '//' in line:
            line = line[:line.index('//')]
        line = line.split()
        if line != []:
            if mark == 1:
                if line[-1] == '*/':
                    mark = 0
                    continue
                else:
                    continue
            if line != [] and line[0] == "/**" and mark == 0:
                if line[-1] != '*/':
                    mark = 1
                else:
                    continue
            if mark == 0 and line != []:
                for i in line:
                    e = e + i + ' '
        if e != '':
            fOut.append(e)
    f.close()
    array = []
    for line in fOut:
        word = ''
        for s in line:
            if s in symbols:
                word += ' ' + s + ' '
            else:
                word += s
        array += word.split()
    array2 = []
    mark = False
    for e in array:
        if mark == True:
            array2[-1] += ' ' + e
            if e[-1] == '"':
                mark = False
        else:
            array2.append(e)
            if e[0] == '"':
                mark = True
    f = open(outname, 'w')
    f.write('<tokens>\n')
    dict = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
    for e in array2:
        if e in symbols:
            if e in dict:
                e = dict[e]
            s = '<symbol> ' + e + ' </symbol>'
        elif e in keyword:
            s = '<keyword> ' + e + ' </keyword>'
        elif e.isdigit():
            s = '<integerConstant> ' + e + ' </integerConstant>'
        elif e[0] == '"' and e[-1] == '"':
            s = '<stringConstant> ' + e[1:-1] + ' </stringConstant>'
        else:
            s = '<identifier> ' + e + ' </identifier>'
        f.write(s)
        f.write('\n')
    f.write('</tokens>')
    f.close()


# Constructor
def Constructor(iname, outname, vmname):
    tokenlist = []
    f = open(iname, 'r')
    for line in f:
        if line != '<tokens>\n' and line != '</tokens>\n':
            tokenlist.append(line)
    f.close()
    f2 = open(outname, 'w')
    f2.write('<class>\n')
    f3 = open(vmname, 'w')
    CompileClass(tokenlist, f2, f3)
    f2.write('</class>')
    f2.close()
    f3.close()


# write the exactly next token in order with correct tabs
def tabwrite(f, s):
    global tab
    global i
    i += 1
    f.write('  ' * tab + s)


# write the current token name with correct tabs
def newtabwrite(f, s):
    global tab
    f.write('  ' * tab + s)


# return the token of current index
def token(s):
    return s.split()[0][1:-1]


# return the value of current index
def content(s):
    if token(s)!='stringConstant':
        return s.split()[1]
    else:
        return s[17:-19]


# Compiles a complete class.
def CompileClass(tokenlist, f, vm):
    global i
    global tab
    global className
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    className = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    # print(content(tokenlist[i + 1]))
    while content(tokenlist[i + 1]) == 'static' or content(tokenlist[i + 1]) == 'field':
        CompileClassVarDec(tokenlist, f, vm)
    while content(tokenlist[i + 1]) == 'constructor' or content(tokenlist[i + 1]) == 'function' or content(
            tokenlist[i + 1]) == 'method':
        CompileSubroutine(tokenlist, f, vm)
    tabwrite(f, tokenlist[i + 1])


# Compiles a static declaration or a ?eld declaration.
def CompileClassVarDec(tokenlist, f, vm):
    global i
    global tab
    global symbolTable
    newtabwrite(f, '<classVarDec>\n')
    tab += 1
    kind = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    type = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    name = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    symbolTable.define(name, type, kind)
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])

        name = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        symbolTable.define(name, type, kind)

    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</classVarDec>\n')


# Compiles a complete method, function, or constructor.
def CompileSubroutine(tokenlist, f, vm):
    global i
    global tab
    global name
    global className
    global symbolTable
    newtabwrite(f, '<subroutineDec>\n')
    tab += 1

    functionType = content(tokenlist[i + 1])
    # print(functionType.split()[1])
    tabwrite(f, tokenlist[i + 1])

    tabwrite(f, tokenlist[i + 1])

    name = className + '.' + content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])

    symbolTable.startSubroutine(name)
    symbolTable.scopeChange(name)

    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == ')':
        newtabwrite(f, '<parameterList>\n')
        newtabwrite(f, '</parameterList>\n')
    while content(tokenlist[i + 1]) != ')':
        compileParameterList(tokenlist, f, vm, functionType)
    tabwrite(f, tokenlist[i + 1])
    compileSubroutineBody(tokenlist, f, vm, functionType)
    tab -= 1
    newtabwrite(f, '</subroutineDec>\n')


# Compiles a (possibly empty) parameter list, not including the enclosing ()
def compileParameterList(tokenlist, f, vm, functionType):
    global i
    global tab
    global symbolTable
    newtabwrite(f, '<parameterList>\n')
    tab += 1

    if functionType == "method":
        symbolTable.define("this", "self", 'arg')
    type = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    name = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    symbolTable.define(name, type, 'arg')
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        type = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        name = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        symbolTable.define(name, type, 'arg')
    tab -= 1
    newtabwrite(f, '</parameterList>\n')


# Compiles subroutine statements after compiling variables
def compileSubroutineBody(tokenlist, f, vm, functionType):
    global i
    global tab
    newtabwrite(f, '<subroutineBody>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) == 'var':
        compileVarDec(tokenlist, f, vm)
    varNumber = symbolTable.varCount('var')
    vm.write('function ' + name + ' ' + str(varNumber) + '\n')
    pointer(vm, functionType)
    compileStatements(tokenlist, f, vm)
    tabwrite(f, tokenlist[i + 1])
    symbolTable.scopeChange(0)
    tab -= 1
    newtabwrite(f, '</subroutineBody>\n')


def pointer(vm, functionType):
    if functionType == "method":
        vm.write('push argument 0\n')
        vm.write('pop pointer 0\n')
    if functionType == 'constructor':
        classVars = symbolTable.classCount('field')
        vm.write('push ' + 'constant ' + str(classVars) + '\n')
        vm.write('call Memory.alloc 1\n')
        vm.write('pop pointer 0\n')


# Compiles a var declaration
def compileVarDec(tokenlist, f, vm):
    global i
    global tab
    newtabwrite(f, '<varDec>\n')
    tab += 1

    kind = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    type = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    name = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    symbolTable.define(name, type, kind)

    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        name = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        symbolTable.define(name, type, kind)
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</varDec>\n')


# Compiles a sequence of statements, not including the enclosing {}
def compileStatements(tokenlist, f, vm):
    global i
    global tab
    newtabwrite(f, '<statements>\n')
    tab += 1
    statelist = ['do', 'while', 'if', 'return', 'let']
    while content(tokenlist[i + 1]) in statelist:
        if content(tokenlist[i + 1]) == 'do':
            compileDo(tokenlist, f, vm)
        elif content(tokenlist[i + 1]) == 'if':
            compileIf(tokenlist, f, vm)
        elif content(tokenlist[i + 1]) == 'while':
            compileWhile(tokenlist, f, vm)
        elif content(tokenlist[i + 1]) == 'return':
            compileReturn(tokenlist, f, vm)
        elif content(tokenlist[i + 1]) == 'let':
            compileLet(tokenlist, f, vm)
    tab -= 1
    newtabwrite(f, '</statements>\n')


# Compiles a let statement.
def compileLet(tokenlist, f, vm):
    global i
    global tab
    newtabwrite(f, '<letStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    array = 0
    name = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == '[':
        array = 1
        tabwrite(f, tokenlist[i + 1])
        compileExpression(tokenlist, f, vm)
        tabwrite(f, tokenlist[i + 1])

        if name in symbolTable.currentScope:
            if symbolTable.kindOf(name) == 'var':
                vm.write('push ' + 'local ' + str(symbolTable.indexOf(name)) + '\n')
            elif symbolTable.kindOf(name) == 'arg':
                vm.write('push ' + 'argument ' + str(symbolTable.indexOf(name)) + '\n')
        else:
            if symbolTable.kindOf(name) == 'static':
                vm.write('push ' + 'static ' + str(symbolTable.indexOf(name)) + '\n')
            else:
                vm.write('push ' + 'this ' + str(symbolTable.indexOf(name)) + '\n')
        vm.write('add\n')
    tabwrite(f, tokenlist[i + 1])
    compileExpression(tokenlist, f, vm)
    if array == 1:
        vm.write('pop temp 0\n')
        vm.write('pop pointer 1\n')
        vm.write('push temp 0\n')
        vm.write('pop that 0\n')
    else:
        if name in symbolTable.currentScope:
            if symbolTable.kindOf(name) == 'var':
                vm.write('pop ' + 'local ' + str(symbolTable.indexOf(name)) + '\n')
            elif symbolTable.kindOf(name) == 'arg':
                vm.write('pop ' + 'argument ' + str(symbolTable.indexOf(name)) + '\n')
        else:
            if symbolTable.kindOf(name) == 'static':
                vm.write('pop ' + 'static ' + str(symbolTable.indexOf(name)) + '\n')
            else:
                vm.write('pop ' + 'this ' + str(symbolTable.indexOf(name)) + '\n')
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</letStatement>\n')


# Compiles a return statement.
def compileReturn(tokenlist, f, vm):
    global i
    global tab
    newtabwrite(f, '<returnStatement>\n')
    tab += 1
    para = 0
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) != ';':
        para = 1
        compileExpression(tokenlist, f, vm)
    if para == 0:
        vm.write('push constant 0\n')
    vm.write('return\n')
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</returnStatement>\n')


# Compiles a while statement.
def compileWhile(tokenlist, f, vm):
    global i
    global tab
    global symbolTable
    newtabwrite(f, '<whileStatement>\n')
    tab += 1
    currentWhile = symbolTable.While
    symbolTable.While += 1
    vm.write('label WHILE_EXP' + str(currentWhile) + '\n')
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileExpression(tokenlist, f, vm)
    vm.write('not\n')
    vm.write('if-goto WHILE_END' + str(currentWhile) + '\n')
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileStatements(tokenlist, f, vm)
    vm.write('goto WHILE_EXP' + str(currentWhile) + '\n')
    vm.write('label WHILE_END' + str(currentWhile) + '\n')
    tabwrite(f, tokenlist[i + 1])

    tab -= 1
    newtabwrite(f, '</whileStatement>\n')


# Compiles a do statement.
def compileDo(tokenlist, f, vm):
    global i
    global tab
    newtabwrite(f, '<doStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    compileSubroutineCall(tokenlist, f, vm)
    vm.write('pop ' + 'temp' + ' ' + str(0) + '\n')
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</doStatement>\n')


# Compiles the function call by subroutine.
def compileSubroutineCall(tokenlist, f, vm):
    global i
    global tab
    global symbolTable
    global className
    clsName = content(tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    lcls = 0
    if content(tokenlist[i + 1]) == '.':
        tabwrite(f, tokenlist[i + 1])
        subName = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        if (clsName in symbolTable.currentScope or clsName in symbolTable.classScope):
            if clsName in symbolTable.currentScope:
                if symbolTable.kindOf(clsName) == 'var':
                    vm.write('push ' + 'local ' + str(symbolTable.indexOf(clsName)) + '\n')
                elif symbolTable.kindOf(clsName) == 'arg':
                    vm.write('push ' + 'argument ' + str(symbolTable.indexOf(clsName)) + '\n')
            else:
                if symbolTable.kindOf(clsName) == 'static':
                    vm.write('push ' + 'static ' + str(symbolTable.indexOf(clsName)) + '\n')
                else:
                    vm.write('push ' + 'this ' + str(symbolTable.indexOf(clsName)) + '\n')
            name = symbolTable.typeOf(clsName) + '.' + subName
            lcls += 1
        else:
            name = clsName + '.' + subName
    else:
        vm.write('push pointer 0\n')
        lcls += 1
        name = className + '.' + clsName
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) != ')':
        lcls += compileExpressionList(tokenlist, f, vm)
    else:
        newtabwrite(f, '<expressionList>\n')
        newtabwrite(f, '</expressionList>\n')
    vm.write('call ' + name + ' ' + str(lcls) + '\n')
    tabwrite(f, tokenlist[i + 1])


# Compiles a (possibly empty) comma-separated list of expressions.
def compileExpressionList(tokenlist, f, vm):
    global i
    global tab
    count = 0
    newtabwrite(f, '<expressionList>\n')
    tab += 1
    if content(tokenlist[i + 1]) != ')':
        compileExpression(tokenlist, f, vm)
        count += 1
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        compileExpression(tokenlist, f, vm)
        count += 1
    tab -= 1
    newtabwrite(f, '</expressionList>\n')
    return count


# Compiles a ifstatement.
def compileIf(tokenlist, f, vm):
    global i
    global tab
    global symbolTable
    newtabwrite(f, '<ifStatement>\n')
    tab += 1
    currentIf=symbolTable.If
    symbolTable.If += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileExpression(tokenlist, f, vm)
    tabwrite(f, tokenlist[i + 1])
    vm.write('if-goto IF_TRUE' + str(currentIf) + ' \n')
    vm.write('goto IF_FALSE' + str(currentIf) + '\n')
    vm.write('label IF_TRUE' + str(currentIf) + '\n')
    tabwrite(f, tokenlist[i + 1])
    compileStatements(tokenlist, f, vm)
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == 'else':
        vm.write('goto IF_END' + str(currentIf) + '\n')
        vm.write('label IF_FALSE' + str(currentIf) + '\n')
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        compileStatements(tokenlist, f, vm)
        tabwrite(f, tokenlist[i + 1])
        vm.write('label IF_END' + str(currentIf) + '\n')
    else:
        vm.write('label IF_FALSE' + str(currentIf) + '\n')

    tab -= 1
    newtabwrite(f, '</ifStatement>\n')


# Compiles an expression.
def compileExpression(tokenlist, f, vm):
    global i
    global tab
    newtabwrite(f, '<expression>\n')
    tab += 1
    compileTerm(tokenlist, f, vm)
    bioplist = ['+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;']
    while content(tokenlist[i + 1]) in bioplist:
        op = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        compileTerm(tokenlist, f, vm)
        if op == '+':
            vm.write('add\n')
        elif op == '-':
            vm.write('sub\n')
        elif op == '*':
            vm.write('call Math.multiply 2\n')
        elif op == '/':
            vm.write('call Math.divide 2\n')
        elif op == '|':
            vm.write('or\n')
        elif op == '=':
            vm.write('eq\n')
        elif op == '&lt;':
            vm.write('lt\n')
        elif op == '&gt;':
            vm.write('gt\n')
        elif op == '&amp;':
            vm.write('and\n')
    tab -= 1
    newtabwrite(f, '</expression>\n')


# Compiles a term. This routine is faced with a slight diffculty when trying to decide between some of the alternative
# parsing rules. Specifcally, if the current token is an identifer, the routine must distinguish between a variable,
# an array entry, and a subroutine call. A single lookahead token, which may be one of [], (, or . suffces to
#  distinguish between the three possibilities. Any other token is not part of this term and should not be advanced over.
def compileTerm(tokenlist, f, vm):
    global i
    global tab
    global symbolTable
    global className
    newtabwrite(f, '<term>\n')
    tab += 1
    keywordlist = ['true', 'false', 'null', 'this']
    unoplist = ['-', '~']
    if token(tokenlist[i + 1]) == "integerConstant" or token(tokenlist[i + 1]) == "stringConstant" \
            or content(tokenlist[i + 1]) in keywordlist:
        constant = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        if token(tokenlist[i]) == "integerConstant":
            vm.write('push constant ' + constant + '\n')
        elif token(tokenlist[i]) == "stringConstant":
            vm.write('push constant ' + str(len(constant)) + '\n')
            vm.write('call String.new 1\n')
            for e in constant:
                vm.write('push constant ' + str(ord(e)) + '\n')
                vm.write('call String.appendChar 2\n')
        else:
            if constant == 'this':
                vm.write('push pointer 0\n')
            else:
                vm.write('push constant 0\n')
                if constant == 'true':
                    vm.write('not\n')
    elif token(tokenlist[i + 1]) == "identifier":
        lcls = 0
        array = 0
        name = content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        if content(tokenlist[i + 1]) == "[":
            array = 1
            tabwrite(f, tokenlist[i + 1])
            compileExpression(tokenlist, f, vm)
            tabwrite(f, tokenlist[i + 1])
            if (name in symbolTable.currentScope or name in symbolTable.classScope):
                if name in symbolTable.currentScope:
                    if symbolTable.kindOf(name) == 'var':
                        vm.write('push ' + 'local ' + str(symbolTable.indexOf(name)) + '\n')
                    elif symbolTable.kindOf(name) == 'arg':
                        vm.write('push ' + 'argument ' + str(symbolTable.indexOf(name)) + '\n')
                else:
                    if symbolTable.kindOf(name) == 'static':
                        vm.write('push ' + 'static ' + str(symbolTable.indexOf(name)) + '\n')
                    else:
                        vm.write('push ' + 'this ' + str(symbolTable.indexOf(name)) + '\n')
            vm.write('add\n')
        elif content(tokenlist[i + 1]) == "(":
            lcls += 1
            vm.write('push pointer 0\n')
            tabwrite(f, tokenlist[i + 1])
            lcls += compileExpressionList(tokenlist, f, vm)
            tabwrite(f, tokenlist[i + 1])
            vm.write('call ' + className + '.' + name + ' ' + str(lcls) + '\n')
        elif content(tokenlist[i + 1]) == ".":
            tabwrite(f, tokenlist[i + 1])
            subName = content(tokenlist[i + 1])
            tabwrite(f, tokenlist[i + 1])
            if (name in symbolTable.currentScope or name in symbolTable.classScope):
                if name in symbolTable.currentScope:
                    if symbolTable.kindOf(name) == 'var':
                        vm.write('push ' + 'local ' + str(symbolTable.indexOf(name)) + '\n')
                    elif symbolTable.kindOf(name) == 'arg':
                        vm.write('push ' + 'argument ' + str(symbolTable.indexOf(name)) + '\n')
                else:
                    if symbolTable.kindOf(name) == 'static':
                        vm.write('push ' + 'static ' + str(symbolTable.indexOf(name)) + '\n')
                    else:
                        vm.write('push ' + 'this ' + str(symbolTable.indexOf(name)) + '\n')
                name = symbolTable.typeOf(name) + '.' + subName
                lcls += 1
            else:
                name = name + '.' + subName
            tabwrite(f, tokenlist[i + 1])
            lcls+=compileExpressionList(tokenlist, f, vm)
            tabwrite(f, tokenlist[i + 1])
            vm.write('call '+name+' '+str(lcls)+'\n')
        if array==1:
            vm.write('pop pointer 1\n')
            vm.write('push that 0\n')
        else:
            if (name in symbolTable.currentScope or name in symbolTable.classScope):
                if name in symbolTable.currentScope:
                    if symbolTable.kindOf(name) == 'var':
                        vm.write('push ' + 'local ' + str(symbolTable.indexOf(name)) + '\n')
                    elif symbolTable.kindOf(name) == 'arg':
                        vm.write('push ' + 'argument ' + str(symbolTable.indexOf(name)) + '\n')
                else:
                    if symbolTable.kindOf(name) == 'static':
                        vm.write('push ' + 'static ' + str(symbolTable.indexOf(name)) + '\n')
                    else:
                        vm.write('push ' + 'this ' + str(symbolTable.indexOf(name)) + '\n')
    elif content(tokenlist[i + 1]) in unoplist:
        unop=content(tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        compileTerm(tokenlist, f, vm)
        if unop=='-':
            vm.write('neg\n')
        elif unop=='~':
            vm.write('not\n')
    elif content(tokenlist[i + 1]) == '(':
        tabwrite(f, tokenlist[i + 1])
        compileExpression(tokenlist, f, vm)
        tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</term>\n')


path = sys.argv[1]
find = 0
fileroot = []
if path[-5:] != '.jack':
    for root, dirc, file in os.walk(path):
        for e in file:
            if e[-5:] == '.jack':
                find += 1
                print('File found:', e)
                fileroot.append((root, e))
    if find == 0:
        print("No file found!")
        exit()
    confirm = input("Input Y to modify all the file found above OR Press ENTER to quit:")
    if confirm == "Y":
        for files in fileroot:
            i = -1
            tab = 0
            symbolTable = Symbol.table()
            iname = files[0] + files[1]
            outname1 = iname[:-5] + 'T.xml'
            outname2 = iname[:-5] + '.xml'
            vmname = iname[:-5] + '.vm'
            Tokenizer.tokenizer.Constructor(iname, outname1)
            Constructor(outname1, outname2, vmname)

else:
    i = -1
    tab = 0
    symbolTable = Symbol.table()
    outname1 = path[:-5] + 'T.xml'
    outname2 = path[:-5] + '.xml'
    vmname = path[:-5] + '.vm'
    Tokenizer.tokenizer.Constructor(path, outname1)
    Constructor(outname1, outname2,vmname)
