from syntactic.SyntacticalTree import SyntacticalNode

lexicalStream = None
lookahead = None
first = {}
follow = {}
syntacticTree = None

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
        else:
            follow[name] = fList
    #print(first)
    #print(follow)


def parse(l):
    global lexicalStream
    global  lookahead
    lexicalStream = l
    getMapOfFirsts()
    lookahead = nextToken()
    if prog():
        #$print(syntacticTree)
        return True
    else:
        return False

def match(currentNodeLevel, token):
    global  lookahead
    if  lookahead.tokenType == token:
        newTreeNode(currentNodeLevel, token, True)
        lookahead = nextToken()
        #print(lookahead)
        return True
    else:
        return False

def newTreeNode(current, value, leaf):
    global syntacticTree
    newNode = SyntacticalNode(syntacticTree, value, leaf)
    current.addChild(newNode)
    #syntacticTree = newNode
    return newNode

def prog():
    global syntacticTree
    syntacticTree = SyntacticalNode(None, 'prog', False)
    currentNode = syntacticTree
    print(first['prog'])
    if   lookahead.tokenType in first['prog']:
        if classHeaders(currentNode) and classSources(currentNode) and match(currentNode, 'program') and funcBody(currentNode) and match(currentNode, ';'):
            print("prog -> classHeaders classSources 'program' funcBody ';'")
            return True
    return False

def classHeaders(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classHeader', False)
    if   lookahead.tokenType in first['classHeaders']:
        if classDecl(currentNodeLevel) and classHeaders(currentNodeLevel):
            print("classHeaders -> classDecl classHeaders")
            return True
    elif   lookahead.tokenType in follow['classHeaders']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("classHeaders -> EPSILON")
        return True
    return False

def classSources(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classSources', False)
    if   lookahead.tokenType  in first['classSources']:
        if funcDef(currentNodeLevel) and classSources(currentNodeLevel):
            print("classSources -> funcDef classSources")
            return True
    elif   lookahead.tokenType  in follow['classSources']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("classSources -> EPSILON")
        return True
    return False

def classDecl(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDecl', False)
    if   lookahead.tokenType  in first['classDecl']:
        if match(currentNodeLevel, 'class') and match(currentNodeLevel, 'id') and inheritance(currentNodeLevel) and match(currentNodeLevel, '{') and classDeclEntities(currentNodeLevel) and match(currentNodeLevel, '}') and match(currentNodeLevel, ';'):
            print("classDecl -> 'class' 'id' inheritance '{' classDeclEntities '}' ';'")
            return True
    return False

def classDeclEntities(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntities', False)
    if   lookahead.tokenType  in first['classDeclEntities']:
        if classDeclEntity(currentNodeLevel) and classDeclEntities(currentNodeLevel):
            print("classDeclEntities -> classDeclEntity classDeclEntities")
            return True
    elif   lookahead.tokenType  in follow['classDeclEntities']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("classDeclEntities -> EPSILON")
        return True
    return False

def classDeclEntity(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntity', False)
    if   lookahead.tokenType  in first['classDeclEntity']:
        if vType(currentNodeLevel) and match(currentNodeLevel, 'id') and classDeclEntityTail(currentNodeLevel):
            print("classDeclEntity -> type 'id' classDeclEntityTail")
            return True
    return False

def classDeclEntityTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntityTail', False)
    if   lookahead.tokenType  in first['classDeclEntityTail']:
        if match(currentNodeLevel, '(') and fParams(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            print("classDeclEntityTail -> '(' fParams ')' ';'")
            return True
        elif arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("classDeclEntityTail -> arrayDimenssion ';'")
            return True
    return False

def inheritance(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'inheritance', False)
    if   lookahead.tokenType  in first['inheritance']:
        if match(currentNodeLevel, ':') and match(currentNodeLevel, 'id') and multipleInheritance(currentNodeLevel):
            print("inheritance -> ':' 'id' multipleInheritance ")
            return True
    elif   lookahead.tokenType  in follow['inheritance']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("inheritance -> EPSILON")
        return True
    return False

def multipleInheritance(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'multipleInheritance', False)
    if   lookahead.tokenType  in first['multipleInheritance']:
        if match(currentNodeLevel, ',') and match(currentNodeLevel, 'id') and multipleInheritance(currentNodeLevel):
            print("multipleInheritance -> ',' 'id' multipleInheritance ")
            return True
    elif   lookahead.tokenType  in follow['multipleInheritance']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("multipleInheritance -> EPSILON")
        return True
    return False

def funcHead(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcHead', False)
    if   lookahead.tokenType  in first['funcHead']:
        if vType(currentNodeLevel) and match(currentNodeLevel, 'id') and namespace(currentNodeLevel) and match(currentNodeLevel, '(') and fParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            print("funcHead -> type 'id' namespace  '(' fParams ')'")
            return True
    return False

def namespace(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'namespace', False)
    if   lookahead.tokenType  in first['namespace']:
        if match(currentNodeLevel, 'sr') and match(currentNodeLevel, 'id'):
            print("namespace -> 'sr' 'id'")
            return True
    elif   lookahead.tokenType  in follow['namespace']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("namespace -> EPSILON")
        return True
    return False

def funcDef(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcDef', False)
    if   lookahead.tokenType  in first['funcDef']:
        if funcHead(currentNodeLevel) and funcBody(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("funcDef -> funcHead funcBody ';'")
            return True
    return False

def funcBody(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcBody', False)
    if   lookahead.tokenType  in first['funcBody']:
        if match(currentNodeLevel, '{') and statements(currentNodeLevel) and match(currentNodeLevel, '}'):
            print("funcBody -> '{' statements '}'")
            return True
    return False

def statements(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statements', False)
    if   lookahead.tokenType  in first['statements']:
        if statement(currentNodeLevel) and statements(currentNodeLevel):
            print("statements -> statement statements")
            return True
    elif   lookahead.tokenType  in follow['statements']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("statements -> EPSILON")
        return True
    return False

def arrayDimenssion(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arrayDimenssion', False)
    if   lookahead.tokenType  in first['arrayDimenssion']:
        if arraySize(currentNodeLevel) and arrayDimenssion(currentNodeLevel):
            print("arrayDimenssion -> arraySize arrayDimenssion")
            return True
    elif   lookahead.tokenType  in follow['arrayDimenssion']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("arrayDimenssion -> EPSILON")
        return True
    return False

def statement(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statement', False)
    if   lookahead.tokenType  in first['statement']:
        if match(currentNodeLevel, 'int') and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("statement -> 'int' 'id' arrayDimenssion ';'")
            return True
        elif match(currentNodeLevel, 'float') and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("statement -> 'float' 'id' arrayDimenssion ';'")
            return True
        elif varAssignOrDecl(currentNodeLevel):
            print("statement -> varAssignOrDecl")
            return True
        elif match(currentNodeLevel, 'if') and match(currentNodeLevel, '(') and expr(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, 'then') and statBlock(currentNodeLevel) and match(currentNodeLevel, 'else') and statBlock(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("statement -> 'if' '(' expr ')' 'then' statBlock 'else' statBlock ';'")
            return True
        elif match(currentNodeLevel, 'for') and match(currentNodeLevel, '(') and vType(currentNodeLevel) and match(currentNodeLevel, 'id') and assignOp(currentNodeLevel) and expr(currentNodeLevel) and match(currentNodeLevel, ';') and relExpr(currentNodeLevel) and match(currentNodeLevel, ';') and assignStat(currentNodeLevel) and match(currentNodeLevel, ')') and statBlock(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("statement -> 'for' '(' type 'id' assignOp expr ';' relExpr ';' assignStat ')' statBlock ';'")
            return True
        elif match(currentNodeLevel, 'get') and match(currentNodeLevel, '(') and variable(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            print("statement -> 'get' '(' variable ')' ';'")
            return True
        elif match(currentNodeLevel, 'put') and match(currentNodeLevel, '(') and expr(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            print("statement -> 'put' '(' expr ')' ';'")
            return True
        elif match(currentNodeLevel, 'return') and match(currentNodeLevel, '(') and expr(currentNodeLevel) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            print("statement -> 'return' '(' expr ')' ';'")
            return True
    return False

def varAssignOrDecl(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'varAssignOrDecl', False)
    if   lookahead.tokenType  in first['varAssignOrDecl']:
        if match(currentNodeLevel, 'id') and varAssignOrDeclTail(currentNodeLevel):
            print("varAssignOrDecl -> 'id' varAssignOrDeclTail")
            return True
    return False

def varAssignOrDeclTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'varAssignOrDeclTail', False)
    if   lookahead.tokenType  in first['varAssignOrDeclTail']:
        if match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("varAssignOrDeclTail -> 'id' arrayDimenssion ';'")
            return True
        elif idnests(currentNodeLevel) and indices(currentNodeLevel) and assignOp(currentNodeLevel) and expr(currentNodeLevel) and match(currentNodeLevel, ';'):
            print("varAssignOrDeclTail -> idnests indices assignOp expr ';'")
            return True
    return False

def assignStat(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'assignStat', False)
    if   lookahead.tokenType  in first['assignStat']:
        if variable(currentNodeLevel) and assignOp(currentNodeLevel) and expr(currentNodeLevel):
            print("assignStat -> variable assignOp expr")
            return True
    return False

def statBlock(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statBlock', False)
    if   lookahead.tokenType  in first['statBlock']:
        if match(currentNodeLevel, '{') and statements(currentNodeLevel) and match(currentNodeLevel, '}'):
            print("statBlock -> '{' statements '}'")
            return True
        elif statement(currentNodeLevel):
            print("statBlock -> statement")
            return True
    elif   lookahead.tokenType  in follow['statBlock']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("statBlock -> EPSILON")
        return True
    return False

def expr(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'expr', False)
    if   lookahead.tokenType  in first['expr']:
        if arithExpr(currentNodeLevel) and exprTail(currentNodeLevel):
            print("expr -> arithExpr exprTail")
            return True
    return False

def exprTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'exprTail', False)
    if   lookahead.tokenType  in first['exprTail']:
        if relOp(currentNodeLevel) and arithExpr(currentNodeLevel):
            print("exprTail -> relOp arithExpr")
            return True
    elif   lookahead.tokenType  in follow['exprTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("exprTail -> EPSILON")
        return True
    return False

def relExpr(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'relExpr', False)
    if   lookahead.tokenType  in first['relExpr']:
        if arithExpr(currentNodeLevel) and relOp(currentNodeLevel) and arithExpr(currentNodeLevel):
            print("relExpr -> arithExpr relOp arithExpr")
            return True
    return False

def arithExpr(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arithExpr', False)
    if   lookahead.tokenType  in first['arithExpr']:
        if term(currentNodeLevel) and arithExprTail(currentNodeLevel):
            print("arithExpr -> term relOp")
            return True
    return False

def arithExprTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arithExprTail', False)
    if   lookahead.tokenType  in first['arithExprTail']:
        if addOp(currentNodeLevel) and term(currentNodeLevel) and arithExprTail(currentNodeLevel):
            print("arithExprTail -> addOp term arithExprTail ")
            return True
    elif   lookahead.tokenType  in follow['arithExprTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("arithExprTail -> EPSILON")
        return True
    return False

def sign(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'sign', False)
    if   lookahead.tokenType  in first['sign']:
        if match(currentNodeLevel, '+'):
            print("sign -> '+'")
            return True
        if match(currentNodeLevel, '-'):
            print("sign -> '-'")
            return True
    return False

def term(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'term', False)
    if   lookahead.tokenType  in first['term']:
        if factor(currentNodeLevel) and termTail(currentNodeLevel):
            print("term -> factor termTail")
            return True
    return False

def termTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'termTail', False)
    if   lookahead.tokenType  in first['termTail']:
        if multOp(currentNodeLevel) and factor(currentNodeLevel) and termTail(currentNodeLevel):
            print("termTail -> multOp factor termTail")
            return True
    elif   lookahead.tokenType  in follow['termTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("termTail -> EPSILON")
        return True
    return False

def factor(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'factor', False)
    if   lookahead.tokenType  in first['factor']:
        if variableOrFuncCall(currentNodeLevel):
            print("factor -> variableOrFuncCall")
            return True
        elif match(currentNodeLevel, 'intNum'):
            print("factor -> intNum")
            return True
        elif match(currentNodeLevel, 'floatNum'):
            print("factor -> floatNum")
            return True
        elif match(currentNodeLevel, '(') and arithExpr(currentNodeLevel) and match(currentNodeLevel, ')'):
            print("factor -> '(' arithExpr ')'")
            return True
        elif match(currentNodeLevel, 'not') and factor(currentNodeLevel):
            print("factor -> 'not' factor")
            return True
        elif sign(currentNodeLevel) and factor(currentNodeLevel):
            print("factor -> sign factor")
            return True
    return False

def variableOrFuncCall(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variableOrFuncCall', False)
    if   lookahead.tokenType  in first['variableOrFuncCall']:
        if match(currentNodeLevel, 'id') and idnests(currentNodeLevel) and variableOrFuncCallTail(currentNodeLevel):
            print("variableOrFuncCall -> 'id' idnests variableOrFuncCallTail")
            return True
    return False

def variableOrFuncCallTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variableOrFuncCallTail', False)
    print(first['variableOrFuncCallTail'])
    if   lookahead.tokenType  in first['variableOrFuncCallTail']:
        if indices(currentNodeLevel):
            print("variableOrFuncCallTail -> indices")
            return True
        elif match(currentNodeLevel, '(') and aParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            print("variableOrFuncCallTail -> '(' aParams ')'")
            return True
    elif lookahead.tokenType  in follow['variableOrFuncCallTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("variableOrFuncCallTail -> EPSILON")
        return True
    return False

def variable(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variable', False)
    if   lookahead.tokenType  in first['variable']:
        if match(currentNodeLevel, 'id') and idnests(currentNodeLevel) and indices(currentNodeLevel):
            print("variable -> 'id' idnests indices")
            return True
    return False

def idnests(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnests', False)
    if   lookahead.tokenType  in first['idnests']:
        if idnest(currentNodeLevel) and idnests(currentNodeLevel):
            print("idnests -> idnest idnests")
            return True
    elif lookahead.tokenType  in follow['idnests']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("idnests -> EPSILON")
        return True
    return False

def indices(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'indices', False)
    if   lookahead.tokenType  in first['indices']:
        if indice(currentNodeLevel) and indices(currentNodeLevel):
            print("indices -> indice indices")
            return True
    elif lookahead.tokenType  in follow['indices']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("indices -> EPSILON")
        return True
    return False

def idnest(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnest', False)
    if   lookahead.tokenType  in first['idnest']:
        if idnestHead(currentNodeLevel) and match(currentNodeLevel, 'id'):
            print("idnest -> idnestHead 'id'")
            return True
    return False

def idnestHead(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnestHead', False)
    if   lookahead.tokenType  in first['idnestHead']:
        if match(currentNodeLevel, '.') and idnestHeadTail(currentNodeLevel):
            print("idnestHead -> '.' idnestHeadTail")
            return True
    return False

def idnestHeadTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnestHeadTail', False)
    if   lookahead.tokenType  in first['idnestHeadTail']:
        if indices(currentNodeLevel):
            print("idnestHeadTail -> indices")
            return True
        elif match(currentNodeLevel, '(') and aParams(currentNodeLevel) and match(currentNodeLevel, ')'):
            print("idnestHeadTail -> '(' aParams ')'")
            return True
    elif  lookahead.tokenType  in follow['idnestHeadTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("idnestHeadTail -> EPSILON")
        return True
    return False

def indice(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'indice', False)
    if   lookahead.tokenType  in first['indice']:
        if match(currentNodeLevel, '[') and arithExpr(currentNodeLevel) and match(currentNodeLevel, ']'):
            print("indice -> '[' arithExpr ']'")
            return True
    return False

def arraySize(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arraySize', False)
    if   lookahead.tokenType  in first['arraySize']:
        if match(currentNodeLevel, '[') and match(currentNodeLevel, 'intNum') and match(currentNodeLevel, ']'):
            print("arraySize -> '[' 'intNum' ']'")
            return True
    return False

def vType(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'type', False)
    if   lookahead.tokenType  in first['type']:
        if match(currentNodeLevel, 'int'):
            print("type -> 'int'")
            return True
        elif match(currentNodeLevel, 'float'):
            print("type -> 'float'")
            return True
        elif match(currentNodeLevel, 'id'):
            print("type -> 'id'")
            return True
    return False

def fParams(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParams', False)
    if   lookahead.tokenType  in first['fParams']:
        if vType(currentNodeLevel) and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel) and fParamsTailList(currentNodeLevel):
            print("fParams -> type 'id' arrayDimenssion fParamsTailList")
            return True
    elif   lookahead.tokenType  in follow['fParams']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("fParams -> EPSILON")
        return True
    return False

def aParams(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParams', False)
    if   lookahead.tokenType  in first['aParams']:
        if expr(currentNodeLevel) and aParamsTailLt(currentNodeLevel):
            print("aParams -> expr aParamsTailLt")
            return True
    elif   lookahead.tokenType  in follow['aParams']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("aParams -> EPSILON")
        return True
    return False

def fParamsTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParamsTail', False)
    if   lookahead.tokenType  in first['fParamsTail']:
        if match(currentNodeLevel, ',') and vType(currentNodeLevel) and match(currentNodeLevel, 'id') and arrayDimenssion(currentNodeLevel):
            print("fParamsTail -> ',' type 'id' arrayDimenssion")
            return True
    return False

def aParamsTail(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParamsTail', False)
    if   lookahead.tokenType  in first['aParamsTail']:
        if match(currentNodeLevel, ',') and expr(currentNodeLevel):
            print("aParamsTail -> ',' expr")
            return True
    return False

def fParamsTailList(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParamsTailList', False)
    if   lookahead.tokenType  in first['fParamsTailList']:
        if fParamsTail(currentNodeLevel) and fParamsTailList(currentNodeLevel):
            print("fParamsTailList -> fParamsTail fParamsTailList")
            return True
    elif   lookahead.tokenType  in follow['fParamsTailList']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("fParamsTailList -> EPSILON")
        return True
    return False

def aParamsTailLt(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParamsTailLt', False)
    if   lookahead.tokenType  in first['aParams']:
        if aParamsTail(currentNodeLevel) and aParamsTailLt(currentNodeLevel):
            print("aParamsTailLt -> aParamsTail aParamsTailLt")
            return True
    elif   lookahead.tokenType  in follow['aParams']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        print("aParamsTailLt -> EPSILON")
        return True
    return False

def assignOp(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'assignOp', False)
    if   lookahead.tokenType  in first['assignOp']:
        if match(currentNodeLevel, '='):
            print("assignOp -> '='")
            return True
    return False

def relOp(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'relOp', False)
    if   lookahead.tokenType  in first['relOp']:
        if match(currentNodeLevel, 'eq'):
            print("relOp -> 'eq'")
            return True
        elif match(currentNodeLevel, 'neq'):
            print("relOp -> 'neq'")
            return True
        elif match(currentNodeLevel, 'lt'):
            print("relOp -> 'lt'")
            return True
        elif match(currentNodeLevel, 'gt'):
            print("relOp -> 'gt'")
            return True
        elif match(currentNodeLevel, 'leq'):
            print("relOp -> 'leq'")
            return True
        elif match(currentNodeLevel, 'geq'):
            print("relOp -> 'geq'")
            return True
    return False

def addOp(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'addOp', False)
    if   lookahead.tokenType  in first['addOp']:
        if match(currentNodeLevel, '+'):
            print("addOp -> '+'")
            return True
        if match(currentNodeLevel, '-'):
            print("addOp -> '-'")
            return True
        if match(currentNodeLevel, 'or'):
            print("addOp -> 'or'")
            return True
    return False

def multOp(currentNodeLevel):
    currentNodeLevel = newTreeNode(currentNodeLevel, 'multOp', False)
    print(first['multOp'])
    if   lookahead.tokenType  in first['multOp']:
        if match(currentNodeLevel, '*'):
            print("multOp -> '*'")
            return True
        if match(currentNodeLevel, '/'):
            print("multOp -> '/'")
            return True
        if match(currentNodeLevel, 'and'):
            print("multOp -> 'and'")
            return True
    return False







        