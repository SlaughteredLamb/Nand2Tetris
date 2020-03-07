import sys
import os

#Constructor
def Constructor(iname, outname):
    tokenlist = []
    f = open(iname, 'r')
    for line in f:
        if line != '<tokens>\n' and line != '</tokens>\n':
            tokenlist.append(line)
    f.close()
    f2 = open(outname, 'w')
    f2.write('<class>\n')
    CompileClass(tokenlist, f2)
    f2.write('</class>')
    f2.close()

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
    return s.split()[1]

# Compiles a complete class.
def CompileClass(tokenlist, f):
    global i
    global tab
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    # print(content(tokenlist[i + 1]))
    while content(tokenlist[i + 1]) == 'static' or content(tokenlist[i + 1]) == 'field':
        CompileClassVarDec(tokenlist, f)
    while content(tokenlist[i + 1]) == 'constructor' or content(tokenlist[i + 1]) == 'function' or content(
            tokenlist[i + 1]) == 'method':
        CompileSubroutine(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])

# Compiles a static declaration or a ?eld declaration.
def CompileClassVarDec(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<classVarDec>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</classVarDec>\n')

#Compiles a complete method, function, or constructor.
def CompileSubroutine(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<subroutineDec>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == ')':
        newtabwrite(f, '<parameterList>\n')
        newtabwrite(f, '</parameterList>\n')
    while content(tokenlist[i + 1]) != ')':
        compileParameterList(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    compileSubroutineBody(tokenlist, f)
    tab -= 1
    newtabwrite(f, '</subroutineDec>\n')

#Compiles a (possibly empty) parameter list, not including the enclosing ()
def compileParameterList(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<parameterList>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</parameterList>\n')

#Compiles subroutine statements after compiling variables
def compileSubroutineBody(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<subroutineBody>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) == 'var':
        compileVarDec(tokenlist, f)
    compileStatements(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</subroutineBody>\n')

#Compiles a var declaration
def compileVarDec(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<varDec>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</varDec>\n')

#Compiles a sequence of statements, not including the enclosing {}
def compileStatements(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<statements>\n')
    tab += 1
    statelist = ['do', 'while', 'if', 'return', 'let']
    while content(tokenlist[i + 1]) in statelist:
        if content(tokenlist[i + 1]) == 'do':
            compileDo(tokenlist, f)
        elif content(tokenlist[i + 1]) == 'if':
            compileIf(tokenlist, f)
        elif content(tokenlist[i + 1]) == 'while':
            compileWhile(tokenlist, f)
        elif content(tokenlist[i + 1]) == 'return':
            compileReturn(tokenlist, f)
        elif content(tokenlist[i + 1]) == 'let':
            compileLet(tokenlist, f)
    tab -= 1
    newtabwrite(f, '</statements>\n')

#Compiles a let statement.
def compileLet(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<letStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == '[':
        tabwrite(f, tokenlist[i + 1])
        compileExpression(tokenlist, f)
        tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileExpression(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</letStatement>\n')

#Compiles a return statement.
def compileReturn(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<returnStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    while content(tokenlist[i + 1]) != ';':
        compileExpression(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</returnStatement>\n')

#Compiles a while statement.
def compileWhile(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<whileStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileExpression(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileStatements(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</whileStatement>\n')

#Compiles a do statement.
def compileDo(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<doStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    compileSubroutineCall(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</doStatement>\n')

#Compiles the function call by subroutine.
def compileSubroutineCall(tokenlist, f):
    global i
    global tab
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == '.':
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) != ')':
        compileExpressionList(tokenlist, f)
    else:
        newtabwrite(f, '<expressionList>\n')
        newtabwrite(f, '</expressionList>\n')
    tabwrite(f, tokenlist[i + 1])

#Compiles a (possibly empty) comma-separated list of expressions.
def compileExpressionList(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<expressionList>\n')
    tab += 1
    if content(tokenlist[i + 1])!=')':
        compileExpression(tokenlist, f)
    while content(tokenlist[i + 1]) == ',':
        tabwrite(f, tokenlist[i + 1])
        compileExpression(tokenlist, f)
    tab -= 1
    newtabwrite(f, '</expressionList>\n')

#Compiles a ifstatement.
def compileIf(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<ifStatement>\n')
    tab += 1
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileExpression(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    tabwrite(f, tokenlist[i + 1])
    compileStatements(tokenlist, f)
    tabwrite(f, tokenlist[i + 1])
    if content(tokenlist[i + 1]) == 'else':
        tabwrite(f, tokenlist[i + 1])
        tabwrite(f, tokenlist[i + 1])
        compileStatements(tokenlist, f)
        tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</ifStatement>\n')

#Compiles an expression.
def compileExpression(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<expression>\n')
    tab += 1
    compileTerm(tokenlist, f)
    bioplist = ['+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;']
    while content(tokenlist[i + 1]) in bioplist:
        tabwrite(f, tokenlist[i + 1])
        compileTerm(tokenlist, f)
    tab -= 1
    newtabwrite(f, '</expression>\n')

# Compiles a term. This routine is faced with a slight dif?culty when trying to decide between some of the alternative
# parsing rules. Speci?cally, if the current token is an identi?er, the routine must distinguish between a variable,
# an array entry, and a subroutine call. A single lookahead token, which may be one of [], (, or . suf?ces to
#  distinguish between the three possibilities. Any other token is not part of this term and should not be advanced over.
def compileTerm(tokenlist, f):
    global i
    global tab
    newtabwrite(f, '<term>\n')
    tab += 1
    keywordlist = ['true', 'false', 'null', 'this']
    unoplist = ['-', '~']
    if token(tokenlist[i + 1]) == "integerConstant" or token(tokenlist[i + 1]) == "stringConstant" \
            or content(tokenlist[i + 1]) in keywordlist:
        tabwrite(f, tokenlist[i + 1])
    elif token(tokenlist[i + 1]) == "identifier":
        tabwrite(f, tokenlist[i + 1])
        if content(tokenlist[i + 1]) == "[":
            tabwrite(f, tokenlist[i + 1])
            compileExpression(tokenlist, f)
            tabwrite(f, tokenlist[i + 1])
        if content(tokenlist[i + 1]) == "(":
            tabwrite(f, tokenlist[i + 1])
            compileExpressionList(tokenlist, f)
            tabwrite(f, tokenlist[i + 1])
        if content(tokenlist[i + 1]) == ".":
            tabwrite(f, tokenlist[i + 1])
            tabwrite(f, tokenlist[i + 1])
            tabwrite(f, tokenlist[i + 1])
            compileExpressionList(tokenlist, f)
            tabwrite(f, tokenlist[i + 1])
    elif content(tokenlist[i + 1]) in unoplist:
        tabwrite(f, tokenlist[i + 1])
        compileTerm(tokenlist, f)
    elif content(tokenlist[i + 1]) == '(':
        tabwrite(f, tokenlist[i + 1])
        compileExpression(tokenlist, f)
        tabwrite(f, tokenlist[i + 1])
    tab -= 1
    newtabwrite(f, '</term>\n')


path = sys.argv[1]
find = 0
fileroot = []
if path[-5:] != 'T.xml':
    for root, dirc, file in os.walk(path):
        for e in file:
            if e[-5:] == 'T.xml':
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
            iname = files[0] + files[1]
            outname = iname[:-5] + '.xml'
            Constructor(iname, outname)
else:
    i = -1
    tab = 0
    outname = path[:-5] + '.xml'
    Constructor(path, outname)
    print(outname)
