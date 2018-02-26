from syntactic.SyntacticalTree import SyntacticalNode

lexicalStream = None
lookahead = None
first = {}
follow = {}
syntacticTree = None
outFile = None
errorFile = None

def nextToken():
    global lexicalStream
    return lexicalStream.nextToken()

def getMapOfFirsts():
    f = open('syntactic/resources/first_follow_list.txt', 'r', -1, 'utf-8')
    for line in f.readlines():
        parts = line.split(' ')
        name = parts[1][1:-1]
        fList = parts[3][1:-2].split('|')
        if parts[0] == 'FIRST':
            first[name] = fList
            follow[name] = []
        else:
            follow[name] = fList
    f.close()


def parse(l, outputFileStream, errorFileStream):
    global lexicalStream, lookahead, outputDerivation, outFile, errorFile
    outFile = outputFileStream
    errorFile = errorFileStream
    lexicalStream = l
    getMapOfFirsts()
    lookahead = nextToken()
    outputDerivation = 'prog '
    if prog():
        writeOutput()
        return True
    else:
        return False

def logError(msg):
    errorFile.write(msg+'\n')
    print(msg)

def logDerivationRule(line):
    outFile.write(line+'\n')

def skipErrors(firstList, followList, token=''):
    global  lookahead
    if lookahead.tokenType in firstList or ('EPSILON' in firstList and lookahead.tokenType in followList):
        return True
    else:
        error = "Invalid syntax at token: >>'"+str(lookahead.value)+"'<< at index "+str(lookahead.index)
        if token:
            error+= ', expected '+ token
        logError(error)
        while lookahead.tokenType not in firstList and lookahead.tokenType not in followList:
            lookahead = nextToken()
            if 'EPSILON' in firstList and lookahead.value in followList:
                return True
        return True

def match(currentNodeLevel, token, trackBack=False):
    global  lookahead
    if  lookahead.tokenType == token:
        newTreeNode(currentNodeLevel, token, True)
        lookahead = nextToken()
        writeOutput()
        return True
    else:
        skipErrors(first[currentNodeLevel.value], follow[currentNodeLevel.value]+[token], token)
        if token == lookahead.tokenType:
            return match(currentNodeLevel, token)
        return False

def writeOutput():
    derivationOutput(syntacticTree)
    outFile.write('\n')
    #print('\n')

def newTreeNode(current, value, leaf):
    global syntacticTree
    newNode = SyntacticalNode(current, value, leaf)
    current.addChild(newNode)
    #syntacticTree = newNode
    return newNode

def derivationOutput(root):
    if not root.children:
        if root.value != 'EPSILON':
            #print(root.value, end=" ", flush=True)
            outFile.write(root.value+" ")
    else:
        for child in root.children:
            derivationOutput(child)

def prog():
    global syntacticTree
    syntacticTree = SyntacticalNode(None, 'prog', False)
    currentNode = syntacticTree
    if lookahead.tokenType in first['prog']:
        if classHeaders(currentNode) and classSources(currentNode) and match(currentNode, 'program') and funcBody(currentNode) and match(currentNode, ';'):
            logDerivationRule("prog -> classHeaders classSources 'program' funcBody ';'")
            writeOutput()
            return True
    
    return False

def classHeaders(currentNodeLevel):
    if not skipErrors(first['classHeaders'], follow['classHeaders']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classHeader', False)
    if   lookahead.tokenType in first['classHeaders']:
        if classDecl(currentNodeLevel) and classHeaders(currentNodeLevel):
            logDerivationRule("classHeaders -> classDecl classHeaders")
            writeOutput()
            return True
    elif  lookahead.tokenType in follow['classHeaders']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classHeaders -> EPSILON")
        writeOutput()
        return True
    
    return False

def classSources(currentNodeLevel):
    if not skipErrors(first['classSources'], follow['classSources']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classSources', False)
    if   lookahead.tokenType  in first['classSources']:
        if funcDef(currentNodeLevel) and classSources(currentNodeLevel):
            logDerivationRule("classSources -> funcDef classSources")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['classSources']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classSources -> EPSILON")
        writeOutput()
        return True
    
    return False

def classDecl(currentNodeLevel):
    if not skipErrors(first['classDecl'], follow['classDecl']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDecl', False)
    if   lookahead.tokenType  in first['classDecl']:
        if match(currentNodeLevel, 'class') and match(currentNodeLevel, 'id') and inheritance(currentNodeLevel) and match(currentNodeLevel, '{') and classDeclEntities(currentNodeLevel) and match(currentNodeLevel, '}') and match(currentNodeLevel, ';'):
            logDerivationRule("classDecl -> 'class' 'id' inheritance '{' classDeclEntities '}' ';'")
            writeOutput()
            return True
    
    return False

def classDeclEntities(currentNodeLevel):
    if not skipErrors(first['classDeclEntities'], follow['classDeclEntities']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntities', False)
    if   lookahead.tokenType  in first['classDeclEntities']:
        if classDeclEntity(currentNodeLevel) and classDeclEntities(currentNodeLevel):
            logDerivationRule("classDeclEntities -> classDeclEntity classDeclEntities")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['classDeclEntities']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classDeclEntities -> EPSILON")
        writeOutput()
        return True
    
    return False

def classDeclEntity(currentNodeLevel):
    if not skipErrors(first['classDeclEntity'], follow['classDeclEntity']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntity', False)
    if   lookahead.tokenType  in first['classDeclEntity']:
        if vType(currentNodeLevel) and match(currentNodeLevel, 'id') and classDeclEntityTail(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("classDeclEntity -> type 'id' classDeclEntityTail ';'")
            writeOutput()
            return True
    
    return False

def classDeclEntityTail(currentNodeLevel):
    if not skipErrors(first['classDeclEntityTail'], follow['classDeclEntityTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntityTail', False)
    if   lookahead.tokenType  in first['classDeclEntityTail']:
        if match(currentNodeLevel, '(') and fParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            logDerivationRule("classDeclEntityTail -> '(' fParams ')'")
            writeOutput()
            return True
        elif arrayDimenssion(currentNodeLevel):
            logDerivationRule("classDeclEntityTail -> arrayDimenssion")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['classDeclEntityTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classDeclEntityTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def inheritance(currentNodeLevel):
    if not skipErrors(first['inheritance'], follow['inheritance']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'inheritance', False)
    if   lookahead.tokenType  in first['inheritance']:
        if match(currentNodeLevel, ':') and match(currentNodeLevel, 'id') and multipleInheritance(currentNodeLevel):
            logDerivationRule("inheritance -> ':' 'id' multipleInheritance ")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['inheritance']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("inheritance -> EPSILON")
        writeOutput()
        return True
    
    return False

def multipleInheritance(currentNodeLevel):
    if not skipErrors(first['multipleInheritance'], follow['multipleInheritance']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'multipleInheritance', False)
    if   lookahead.tokenType  in first['multipleInheritance']:
        if match(currentNodeLevel, ',') and match(currentNodeLevel, 'id') and multipleInheritance(currentNodeLevel):
            logDerivationRule("multipleInheritance -> ',' 'id' multipleInheritance ")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['multipleInheritance']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("multipleInheritance -> EPSILON")
        writeOutput()
        return True
    
    return False

def funcHead(currentNodeLevel):
    if not skipErrors(first['funcHead'], follow['funcHead']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcHead', False)
    if   lookahead.tokenType  in first['funcHead']:
        if vType(currentNodeLevel) and match(currentNodeLevel, 'id') and namespace(currentNodeLevel) and match(currentNodeLevel, '(') and fParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            logDerivationRule("funcHead -> type 'id' namespace  '(' fParams ')'")
            writeOutput()
            return True
    
    return False

def namespace(currentNodeLevel):
    if not skipErrors(first['namespace'], follow['namespace']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'namespace', False)
    if   lookahead.tokenType  in first['namespace']:
        if match(currentNodeLevel, 'sr') and match(currentNodeLevel, 'id'):
            logDerivationRule("namespace -> 'sr' 'id'")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['namespace']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("namespace -> EPSILON")
        writeOutput()
        return True
    
    return False

def funcDef(currentNodeLevel):
    if not skipErrors(first['funcDef'], follow['funcDef']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcDef', False)
    if   lookahead.tokenType  in first['funcDef']:
        if funcHead(currentNodeLevel) and funcBody(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("funcDef -> funcHead funcBody ';'")
            writeOutput()
            return True
    
    return False

def funcBody(currentNodeLevel):
    if not skipErrors(first['funcBody'], follow['funcBody']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcBody', False)
    if   lookahead.tokenType  in first['funcBody']:
        if match(currentNodeLevel, '{') and statements(currentNodeLevel) and match(currentNodeLevel, '}'):
            logDerivationRule("funcBody -> '{' statements '}'")
            writeOutput()
            return True
    
    return False

def statements(currentNodeLevel):
    if not skipErrors(first['statements'], follow['statements']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statements', False)
    if   lookahead.tokenType  in first['statements']:
        if statement(currentNodeLevel) and statements(currentNodeLevel):
            logDerivationRule("statements -> statement statements")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['statements']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("statements -> EPSILON")
        writeOutput()
        return True
    
    return False

def arrayDimenssion(currentNodeLevel):
    if not skipErrors(first['arrayDimenssion'], follow['arrayDimenssion']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arrayDimenssion', False)
    if   lookahead.tokenType  in first['arrayDimenssion']:
        if arraySize(currentNodeLevel) and arrayDimenssion(currentNodeLevel):
            logDerivationRule("arrayDimenssion -> arraySize arrayDimenssion")
            writeOutput()
            return True
    elif  lookahead.tokenType  in follow['arrayDimenssion']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("arrayDimenssion -> EPSILON")
        writeOutput()
        return True
    
    return False

def statement(currentNodeLevel):
    if not skipErrors(first['statement'], follow['statement']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statement', False)
    if   lookahead.tokenType  in first['statement']:
        if match(currentNodeLevel, 'int') and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'int' 'id' arrayDimenssion ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'float') and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'float' 'id' arrayDimenssion ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'if') and match(currentNodeLevel, '(') and expr(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, 'then') and statBlock(currentNodeLevel) and match(currentNodeLevel, 'else') and statBlock(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'if' '(' expr ')' 'then' statBlock 'else' statBlock ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'for') and match(currentNodeLevel, '(') and vType(currentNodeLevel) and match(currentNodeLevel, 'id') and assignOp(currentNodeLevel) and expr(currentNodeLevel) and match(currentNodeLevel, ';') and relExpr(currentNodeLevel) and match(currentNodeLevel, ';') and assignStat(currentNodeLevel) and match(currentNodeLevel, ')') and statBlock(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'for' '(' type 'id' assignOp expr ';' relExpr ';' assignStat ')' statBlock ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'get') and match(currentNodeLevel, '(') and variable(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'get' '(' variable ')' ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'put') and match(currentNodeLevel, '(') and expr(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'put' '(' expr ')' ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'return') and match(currentNodeLevel, '(') and expr(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            logDerivationRule("statement -> 'return' '(' expr ')' ';'")
            writeOutput()
            return True
        elif varAssignOrDecl(currentNodeLevel):
            logDerivationRule("statement -> varAssignOrDecl")
            writeOutput()
            return True
    
    return False

def varAssignOrDecl(currentNodeLevel):
    if not skipErrors(first['varAssignOrDecl'], follow['varAssignOrDecl']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'varAssignOrDecl', False)
    if   lookahead.tokenType  in first['varAssignOrDecl']:
        if match(currentNodeLevel, 'id') and varAssignOrDeclTail(currentNodeLevel):
            logDerivationRule("varAssignOrDecl -> 'id' varAssignOrDeclTail")
            writeOutput()
            return True
    parent = currentNodeLevel.parent
    parent.children.remove(currentNodeLevel)
    
    return False

def varAssignOrDeclTail(currentNodeLevel):
    if not skipErrors(first['varAssignOrDeclTail'], follow['varAssignOrDeclTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'varAssignOrDeclTail', False)
    if   lookahead.tokenType  in first['varAssignOrDeclTail']:
        if match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("varAssignOrDeclTail -> 'id' arrayDimenssion ';'")
            writeOutput()
            return True
        elif idnests(currentNodeLevel) and indices(currentNodeLevel) and assignOp(currentNodeLevel) and expr(currentNodeLevel) and match(currentNodeLevel, ';'):
            logDerivationRule("varAssignOrDeclTail -> idnests indices assignOp expr ';'")
            writeOutput()
            return True
    
    return False

def assignStat(currentNodeLevel):
    if not skipErrors(first['assignStat'], follow['assignStat']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'assignStat', False)
    if   lookahead.tokenType  in first['assignStat']:
        if variable(currentNodeLevel) and assignOp(currentNodeLevel) and expr(currentNodeLevel):
            logDerivationRule("assignStat -> variable assignOp expr")
            writeOutput()
            return True
    
    return False

def statBlock(currentNodeLevel):
    if not skipErrors(first['statBlock'], follow['statBlock']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statBlock', False)
    if   lookahead.tokenType  in first['statBlock']:
        if match(currentNodeLevel, '{') and statements(currentNodeLevel) and match(currentNodeLevel, '}'):
            logDerivationRule("statBlock -> '{' statements '}'")
            writeOutput()
            return True
        elif statement(currentNodeLevel):
            logDerivationRule("statBlock -> statement")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['statBlock']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("statBlock -> EPSILON")
        writeOutput()
        return True
    
    return False

def expr(currentNodeLevel):
    if not skipErrors(first['expr'], follow['expr']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'expr', False)
    if   lookahead.tokenType  in first['expr']:
        if arithExpr(currentNodeLevel) and exprTail(currentNodeLevel):
            logDerivationRule("expr -> arithExpr exprTail")
            writeOutput()
            return True
    
    return False

def exprTail(currentNodeLevel):
    if not skipErrors(first['exprTail'], follow['exprTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'exprTail', False)
    if   lookahead.tokenType  in first['exprTail']:
        if relOp(currentNodeLevel) and arithExpr(currentNodeLevel):
            logDerivationRule("exprTail -> relOp arithExpr")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['exprTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("exprTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def relExpr(currentNodeLevel):
    if not skipErrors(first['relExpr'], follow['relExpr']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'relExpr', False)
    if   lookahead.tokenType  in first['relExpr']:
        if arithExpr(currentNodeLevel) and relOp(currentNodeLevel) and arithExpr(currentNodeLevel):
            logDerivationRule("relExpr -> arithExpr relOp arithExpr")
            writeOutput()
            return True
    
    return False

def arithExpr(currentNodeLevel):
    if not skipErrors(first['arithExpr'], follow['arithExpr']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arithExpr', False)
    if   lookahead.tokenType  in first['arithExpr']:
        if term(currentNodeLevel) and arithExprTail(currentNodeLevel):
            logDerivationRule("arithExpr -> term relOp")
            writeOutput()
            return True
    
    return False

def arithExprTail(currentNodeLevel):
    if not skipErrors(first['arithExprTail'], follow['arithExprTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arithExprTail', False)
    if   lookahead.tokenType  in first['arithExprTail']:
        if addOp(currentNodeLevel) and term(currentNodeLevel) and arithExprTail(currentNodeLevel):
            logDerivationRule("arithExprTail -> addOp term arithExprTail ")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['arithExprTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("arithExprTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def sign(currentNodeLevel):
    if not skipErrors(first['sign'], follow['sign']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'sign', False)
    if   lookahead.tokenType  in first['sign']:
        if match(currentNodeLevel, '+'):
            logDerivationRule("sign -> '+'")
            writeOutput()
            return True
        if match(currentNodeLevel, '-'):
            logDerivationRule("sign -> '-'")
            writeOutput()
            return True
    
    return False

def term(currentNodeLevel):
    if not skipErrors(first['term'], follow['term']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'term', False)
    if   lookahead.tokenType  in first['term']:
        if factor(currentNodeLevel) and termTail(currentNodeLevel):
            logDerivationRule("term -> factor termTail")
            writeOutput()
            return True
    
    return False

def termTail(currentNodeLevel):
    if not skipErrors(first['termTail'], follow['termTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'termTail', False)
    if   lookahead.tokenType  in first['termTail']:
        if multOp(currentNodeLevel) and factor(currentNodeLevel) and termTail(currentNodeLevel):
            logDerivationRule("termTail -> multOp factor termTail")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['termTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("termTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def factor(currentNodeLevel):
    if not skipErrors(first['factor'], follow['factor']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'factor', False)
    if   lookahead.tokenType  in first['factor']:
        if variableOrFuncCall(currentNodeLevel):
            logDerivationRule("factor -> variableOrFuncCall")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'intNum'):
            logDerivationRule("factor -> intNum")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'floatNum'):
            logDerivationRule("factor -> floatNum")
            writeOutput()
            return True
        elif match(currentNodeLevel, '(') and arithExpr(currentNodeLevel) and match(currentNodeLevel, ')'):
            logDerivationRule("factor -> '(' arithExpr ')'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'not') and factor(currentNodeLevel):
            logDerivationRule("factor -> 'not' factor")
            writeOutput()
            return True
        elif sign(currentNodeLevel) and factor(currentNodeLevel):
            logDerivationRule("factor -> sign factor")
            writeOutput()
            return True
    
    return False

def variableOrFuncCall(currentNodeLevel):
    #if not skipErrors(first['variableOrFuncCall'], follow['variableOrFuncCall']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variableOrFuncCall', False)
    if   lookahead.tokenType  in first['variableOrFuncCall']:
        if match(currentNodeLevel, 'id') and idnests(currentNodeLevel) and variableOrFuncCallTail(currentNodeLevel):
            logDerivationRule("variableOrFuncCall -> 'id' idnests variableOrFuncCallTail")
            writeOutput()
            return True
    parent = currentNodeLevel.parent
    parent.children.remove(currentNodeLevel)
    #
    return False

def variableOrFuncCallTail(currentNodeLevel):
    #if not skipErrors(first['variableOrFuncCallTail'], follow['variableOrFuncCallTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variableOrFuncCallTail', False)
    if   lookahead.tokenType  in first['variableOrFuncCallTail']:
        if match(currentNodeLevel, '(') and aParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            logDerivationRule("variableOrFuncCallTail -> '(' aParams ')'")
            writeOutput()
            return True
        if indices(currentNodeLevel):
            logDerivationRule("variableOrFuncCallTail -> indices")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['variableOrFuncCallTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("variableOrFuncCallTail -> EPSILON")
        writeOutput()
        return True
    #
    return False

def variable(currentNodeLevel):
    if not skipErrors(first['variable'], follow['variable']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variable', False)
    if   lookahead.tokenType  in first['variable']:
        if match(currentNodeLevel, 'id') and idnests(currentNodeLevel) and indices(currentNodeLevel):
            logDerivationRule("variable -> 'id' idnests indices")
            writeOutput()
            return True
    
    return False

def idnests(currentNodeLevel):
    if not skipErrors(first['idnests'], follow['idnests']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnests', False)
    if   lookahead.tokenType  in first['idnests']:
        if idnest(currentNodeLevel) and idnests(currentNodeLevel):
            logDerivationRule("idnests -> idnest idnests")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['idnests']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("idnests -> EPSILON")
        writeOutput()
        return True
    
    return False

def indices(currentNodeLevel):
    if not skipErrors(first['indices'], follow['indices']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'indices', False)
    if   lookahead.tokenType  in first['indices']:
        if indice(currentNodeLevel) and indices(currentNodeLevel):
            logDerivationRule("indices -> indice indices")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['indices']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("indices -> EPSILON")
        writeOutput()
        return True
    parent = currentNodeLevel.parent
    parent.children.remove(currentNodeLevel)
    return False

def idnest(currentNodeLevel):
    if not skipErrors(first['idnest'], follow['idnest']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnest', False)
    if   lookahead.tokenType  in first['idnest']:
        if idnestHead(currentNodeLevel) and match(currentNodeLevel, 'id'):
            logDerivationRule("idnest -> idnestHead 'id'")
            writeOutput()
            return True
    
    return False

def idnestHead(currentNodeLevel):
    if not skipErrors(first['idnestHead'], follow['idnestHead']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnestHead', False)
    if   lookahead.tokenType  in first['idnestHead']:
        if match(currentNodeLevel, '.') and idnestHeadTail(currentNodeLevel):
            logDerivationRule("idnestHead -> '.' idnestHeadTail")
            writeOutput()
            return True
    
    return False

def idnestHeadTail(currentNodeLevel):
    if not skipErrors(first['idnestHeadTail'], follow['idnestHeadTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnestHeadTail', False)
    if   lookahead.tokenType  in first['idnestHeadTail']:
        if indices(currentNodeLevel):
            logDerivationRule("idnestHeadTail -> indices")
            writeOutput()
            return True
        elif match(currentNodeLevel, '(') and aParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            logDerivationRule("idnestHeadTail -> '(' aParams ')'")
            writeOutput()
            return True
    elif  lookahead.tokenType  in follow['idnestHeadTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("idnestHeadTail -> EPSILON")
        writeOutput()
        return True
    return False

def indice(currentNodeLevel):
    if not skipErrors(first['indice'], follow['indice']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'indice', False)
    if   lookahead.tokenType  in first['indice']:
        if match(currentNodeLevel, '[') and arithExpr(currentNodeLevel) and match(currentNodeLevel, ']'):
            logDerivationRule("indice -> '[' arithExpr ']'")
            writeOutput()
            return True
    
    return False

def arraySize(currentNodeLevel):
    if not skipErrors(first['arraySize'], follow['arraySize']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arraySize', False)
    if   lookahead.tokenType  in first['arraySize']:
        if match(currentNodeLevel, '[') and match(currentNodeLevel, 'intNum') and match(currentNodeLevel, ']'):
            logDerivationRule("arraySize -> '[' 'intNum' ']'")
            writeOutput()
            return True
    
    return False

def vType(currentNodeLevel):
    if not skipErrors(first['type'], follow['type']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'type', False)
    if   lookahead.tokenType  in first['type']:
        if match(currentNodeLevel, 'int'):
            logDerivationRule("type -> 'int'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'float'):
            logDerivationRule("type -> 'float'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'id'):
            logDerivationRule("type -> 'id'")
            writeOutput()
            return True
    
    return False

def fParams(currentNodeLevel):
    if not skipErrors(first['fParams'], follow['fParams']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParams', False)
    if   lookahead.tokenType  in first['fParams']:
        if vType(currentNodeLevel) and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and fParamsTailList(currentNodeLevel):
            logDerivationRule("fParams -> type 'id' arrayDimenssion fParamsTailList")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['fParams']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("fParams -> EPSILON")
        writeOutput()
        return True
    
    return False

def aParams(currentNodeLevel):
    if not skipErrors(first['aParams'], follow['aParams']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParams', False)
    if   lookahead.tokenType  in first['aParams']:
        if expr(currentNodeLevel) and aParamsTailList(currentNodeLevel):
            logDerivationRule("aParams -> expr aParamsTailList")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['aParams']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("aParams -> EPSILON")
        writeOutput()
        return True
    
    return False

def fParamsTail(currentNodeLevel):
    if not skipErrors(first['fParamsTail'], follow['fParamsTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParamsTail', False)
    if   lookahead.tokenType  in first['fParamsTail']:
        if match(currentNodeLevel, ',') and vType(currentNodeLevel) and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel):
            logDerivationRule("fParamsTail -> ',' type 'id' arrayDimenssion")
            writeOutput()
            return True
    
    return False

def aParamsTail(currentNodeLevel):
    if not skipErrors(first['aParamsTail'], follow['aParamsTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParamsTail', False)
    if   lookahead.tokenType  in first['aParamsTail']:
        if match(currentNodeLevel, ',') and expr(currentNodeLevel):
            logDerivationRule("aParamsTail -> ',' expr")
            writeOutput()
            return True
    
    return False

def fParamsTailList(currentNodeLevel):
    if not skipErrors(first['fParamsTailList'], follow['fParamsTailList']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParamsTailList', False)
    if   lookahead.tokenType  in first['fParamsTailList']:
        if fParamsTail(currentNodeLevel) and fParamsTailList(currentNodeLevel):
            logDerivationRule("fParamsTailList -> fParamsTail fParamsTailList")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['fParamsTailList']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("fParamsTailList -> EPSILON")
        writeOutput()
        return True
    
    return False

def aParamsTailList(currentNodeLevel):
    if not skipErrors(first['aParamsTailList'], follow['aParamsTailList']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParamsTailList', False)
    if   lookahead.tokenType  in first['aParamsTailList']:
        if aParamsTail(currentNodeLevel) and aParamsTailList(currentNodeLevel):
            logDerivationRule("aParamsTailList -> aParamsTail aParamsTailList")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['aParamsTailList']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("aParamsTailList -> EPSILON")
        writeOutput()
        return True
    return False

def assignOp(currentNodeLevel):
    if not skipErrors(first['assignOp'], follow['assignOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'assignOp', False)
    if   lookahead.tokenType  in first['assignOp']:
        if match(currentNodeLevel, '='):
            logDerivationRule("assignOp -> '='")
            writeOutput()
            return True
    
    return False

def relOp(currentNodeLevel):
    if not skipErrors(first['relOp'], follow['relOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'relOp', False)
    if   lookahead.tokenType  in first['relOp']:
        if match(currentNodeLevel, 'eq'):
            logDerivationRule("relOp -> 'eq'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'neq'):
            logDerivationRule("relOp -> 'neq'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'lt'):
            logDerivationRule("relOp -> 'lt'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'gt'):
            logDerivationRule("relOp -> 'gt'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'leq'):
            logDerivationRule("relOp -> 'leq'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'geq'):
            logDerivationRule("relOp -> 'geq'")
            writeOutput()
            return True
    
    return False

def addOp(currentNodeLevel):
    if not skipErrors(first['addOp'], follow['addOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'addOp', False)
    if   lookahead.tokenType  in first['addOp']:
        if match(currentNodeLevel, '+'):
            logDerivationRule("addOp -> '+'")
            writeOutput()
            return True
        if match(currentNodeLevel, '-'):
            logDerivationRule("addOp -> '-'")
            writeOutput()
            return True
        if match(currentNodeLevel, 'or'):
            logDerivationRule("addOp -> 'or'")
            writeOutput()
            return True
    
    return False

def multOp(currentNodeLevel):
    #if not skipErrors(first['multOp'], follow['multOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'multOp', False)
    if   lookahead.tokenType  in first['multOp']:
        if match(currentNodeLevel, '*'):
            logDerivationRule("multOp -> '*'")
            writeOutput()
            return True
        if match(currentNodeLevel, '/'):
            logDerivationRule("multOp -> '/'")
            writeOutput()
            return True
        if match(currentNodeLevel, 'and'):
            logDerivationRule("multOp -> 'and'")
            writeOutput()
            return True
    return False







        