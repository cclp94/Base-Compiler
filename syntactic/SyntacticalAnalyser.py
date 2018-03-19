from syntactic.SyntaxTree import ConcreteSyntaxNode
from syntactic.SyntaxTree import *

lexicalStream = None
lookahead = None
first = {}
follow = {}
syntacticTree = None
ast = None
outFile = None
errorFile = None

def nextToken():
    global lexicalStream
    token = lexicalStream.nextToken()
    while token and token.tokenType == 'CMT':
        token = lexicalStream.nextToken()
    return token

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
        return ast

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
            if not lookahead:
                return False
            if 'EPSILON' in firstList and lookahead.value in followList:
                return True
        return True

def match(currentNodeLevel, token, astNode = None):
    global  lookahead
    if  lookahead.tokenType == token:
        if astNode:
            astNode[0].setValue(lookahead)
        newTreeNode(currentNodeLevel, token, True)
        lookahead = nextToken()
        writeOutput()
        return True
    else:
        skipErrors(first[currentNodeLevel.value], follow[currentNodeLevel.value]+[token], token)
        if token == lookahead.tokenType:
            return match(currentNodeLevel, token, astNode)
        return False

def writeOutput():
    derivationOutput(syntacticTree)
    outFile.write('\n')
    #print('\n')

def newTreeNode(current, value, leaf):
    global syntacticTree
    newNode = ConcreteSyntaxNode(current, value, leaf)
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
    global syntacticTree, ast
    classHeadersNode = [ClassDeclNode()]
    classSourcesNode = [ClassSourceNode()]
    funcBodyNode = [AbstractSyntaxNode()]
    programNode = [ProgramNode()]
    syntacticTree = ConcreteSyntaxNode(None, 'prog', False)
    currentNode = syntacticTree
    if lookahead.tokenType in first['prog']:
        if classHeaders(currentNode, classHeadersNode) and classSources(currentNode, classSourcesNode) and match(currentNode, 'program', programNode) and funcBody(currentNode, funcBodyNode) and match(currentNode, ';'):
            ast = AbstractSyntaxNode.makeFamily([ProgNode('prog')], [classHeadersNode[0], classSourcesNode[0], AbstractSyntaxNode.makeFamily([programNode[0]],[funcBodyNode[0]])])
            print(ast)
            logDerivationRule("prog -> classHeaders classSources 'program' funcBody ';'")
            writeOutput()
            return True
    
    return False

def classHeaders(currentNodeLevel, astNode):
    if not skipErrors(first['classHeaders'], follow['classHeaders']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classHeader', False)
    declNode = [ClassDeclNode()]
    if   lookahead.tokenType in first['classHeaders']:
        if classDecl(currentNodeLevel, declNode) and classHeaders(currentNodeLevel, declNode):
            if not astNode[0].value:
                astNode[0] = (declNode[0])
            else:
                astNode[0].addSibling(declNode[0])
            logDerivationRule("classHeaders -> classDecl classHeaders")
            writeOutput()
            return True
    elif  lookahead.tokenType in follow['classHeaders']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classHeaders -> EPSILON")
        writeOutput()
        return True
    
    return False

def classSources(currentNodeLevel, astNode):
    if not skipErrors(first['classSources'], follow['classSources']): return False
    funcDefNode = [ClassSourceNode()]
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classSources', False)
    if lookahead.tokenType  in first['classSources']:
        if funcDef(currentNodeLevel, funcDefNode) and classSources(currentNodeLevel, funcDefNode):
            if not astNode[0].value:
                astNode[0] = (funcDefNode[0])
            else:
                astNode[0].addSibling(funcDefNode[0])
            logDerivationRule("classSources -> funcDef classSources")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['classSources']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classSources -> EPSILON")
        writeOutput()
        return True
    
    return False

def classDecl(currentNodeLevel, astNode):
    if not skipErrors(first['classDecl'], follow['classDecl']): return False
    inheritanceNode = [InheritanceNode()]
    classDeclEntitiesNode = [ClassMemberDeclNode()]
    classIdNode = [IdNode()]
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDecl', False)
    if lookahead.tokenType  in first['classDecl']:
        if match(currentNodeLevel, 'class') and match(currentNodeLevel, 'id', classIdNode) and inheritance(currentNodeLevel, inheritanceNode) and match(currentNodeLevel, '{') and classDeclEntities(currentNodeLevel, classDeclEntitiesNode) and match(currentNodeLevel, '}') and match(currentNodeLevel, ';'):
            newNode = AbstractSyntaxNode.makeFamily([ClassDeclNode('classDecl')], [classIdNode[0], inheritanceNode[0], classDeclEntitiesNode[0]])
            astNode[0] = (newNode)
            logDerivationRule("classDecl -> 'class' 'id' inheritance '{' classDeclEntities '}' ';'")
            writeOutput()
            return True
    
    return False

def classDeclEntities(currentNodeLevel, astNode):
    if not skipErrors(first['classDeclEntities'], follow['classDeclEntities']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntities', False)
    classDeclEntityNode = [ClassMemberDeclNode()]
    if lookahead.tokenType  in first['classDeclEntities']:
        if classDeclEntity(currentNodeLevel, classDeclEntityNode) and classDeclEntities(currentNodeLevel, classDeclEntityNode):
            if not astNode[0].value:
                astNode[0] = (classDeclEntityNode[0])
            else:
                astNode[0].addSibling(classDeclEntityNode[0])
            logDerivationRule("classDeclEntities -> classDeclEntity classDeclEntities")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['classDeclEntities']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classDeclEntities -> EPSILON")
        writeOutput()
        return True
    
    return False

def classDeclEntity(currentNodeLevel, astNode):
    if not skipErrors(first['classDeclEntity'], follow['classDeclEntity']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntity', False)
    idNode = [IdNode()]
    typeNode = [TypeNode()]
    if   lookahead.tokenType  in first['classDeclEntity']:
        if vType(currentNodeLevel, typeNode) and match(currentNodeLevel, 'id', idNode) and classDeclEntityTail(currentNodeLevel, typeNode, idNode, astNode) and match(currentNodeLevel, ';'):
            logDerivationRule("classDeclEntity -> type 'id' classDeclEntityTail ';'")
            writeOutput()
            return True
    
    return False

def classDeclEntityTail(currentNodeLevel, typeNode, idNode, astNode):
    if not skipErrors(first['classDeclEntityTail'], follow['classDeclEntityTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'classDeclEntityTail', False)
    functionNode = [FuncParamsNode()]
    VarNode = [ArrayDimenssionNode()]
    if lookahead.tokenType  in first['classDeclEntityTail']:
        if match(currentNodeLevel, '(') and fParams(currentNodeLevel, functionNode) and match(currentNodeLevel, ')'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([ClassMethodNode('methodDecl')], [typeNode[0], idNode[0], functionNode[0]]))
            logDerivationRule("classDeclEntityTail -> '(' fParams ')'")
            writeOutput()
            return True
        elif arrayDimenssion(currentNodeLevel, VarNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([ClassAttributeNode('attributeDecl')], [typeNode[0], idNode[0], VarNode[0]]))
            logDerivationRule("classDeclEntityTail -> arrayDimenssion")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['classDeclEntityTail']:
        astNode[0] = (AbstractSyntaxNode.makeFamily([ClassAttributeNode('attributeDecl')], [typeNode[0], idNode[0]]))
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("classDeclEntityTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def inheritance(currentNodeLevel, astNode):
    if not skipErrors(first['inheritance'], follow['inheritance']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'inheritance', False)
    idNode = [InheritanceNode()]
    multipleInheritanceNode = [IdNode()]
    if lookahead.tokenType  in first['inheritance']:
        if match(currentNodeLevel, ':') and match(currentNodeLevel, 'id', idNode) and multipleInheritance(currentNodeLevel, multipleInheritanceNode):
            astNode[0] = idNode[0]
            astNode[0].addSibling(multipleInheritanceNode[0])
            logDerivationRule("inheritance -> ':' 'id' multipleInheritance ")
            writeOutput()
            return True
    elif lookahead.tokenType in follow['inheritance']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("inheritance -> EPSILON")
        writeOutput()
        return True
    
    return False

def multipleInheritance(currentNodeLevel, astNode):
    if not skipErrors(first['multipleInheritance'], follow['multipleInheritance']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'multipleInheritance', False)
    idNode = [InheritanceNode()]
    if lookahead.tokenType  in first['multipleInheritance']:
        if match(currentNodeLevel, ',') and match(currentNodeLevel, 'id', idNode) and multipleInheritance(currentNodeLevel, idNode):
            if not astNode[0].value:
                astNode[0] = (idNode[0])
            else:
                astNode[0].addSibling(idNode[0])
            logDerivationRule("multipleInheritance -> ',' 'id' multipleInheritance ")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['multipleInheritance']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("multipleInheritance -> EPSILON")
        writeOutput()
        return True
    
    return False

def funcHead(currentNodeLevel, astNode):
    if not skipErrors(first['funcHead'], follow['funcHead']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcHead', False)
    typeNode = [TypeNode()]
    idNode = [IdNode()]
    namespaceNode = [IdNode()]
    fparamsNode = [FuncParamsNode()]
    if lookahead.tokenType  in first['funcHead']:
        if vType(currentNodeLevel, typeNode) and match(currentNodeLevel, 'id', idNode) and namespace(currentNodeLevel, namespaceNode) and match(currentNodeLevel, '(') and fParams(currentNodeLevel, fparamsNode) and match(currentNodeLevel, ')'):
            typeNode[0].addSibling(idNode[0])
            if namespaceNode[0]:
                idNode[0].addSibling(namespaceNode[0])
            idNode[0].addSibling(fparamsNode[0])
            astNode[0] = (idNode[0])
            logDerivationRule("funcHead -> type 'id' namespace  '(' fParams ')'")
            writeOutput()
            return True
    
    return False

def namespace(currentNodeLevel, astNode):
    if not skipErrors(first['namespace'], follow['namespace']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'namespace', False)
    idNode = [IdNode()]
    if lookahead.tokenType  in first['namespace']:
        if match(currentNodeLevel, 'sr') and match(currentNodeLevel, 'id', idNode):
            astNode[0] = (idNode[0])
            logDerivationRule("namespace -> 'sr' 'id'")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['namespace']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("namespace -> EPSILON")
        writeOutput()
        return True
    
    return False

def funcDef(currentNodeLevel, astNode):
    if not skipErrors(first['funcDef'], follow['funcDef']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcDef', False)
    funcHeadNode = [AbstractSyntaxNode()]
    funcBodyNode = [FuncBodyNode()]
    if   lookahead.tokenType  in first['funcDef']:
        if funcHead(currentNodeLevel, funcHeadNode) and funcBody(currentNodeLevel, funcBodyNode) and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([ClassSourceNode('funcDef')], [funcHeadNode[0], funcBodyNode[0]]))
            logDerivationRule("funcDef -> funcHead funcBody ';'")
            writeOutput()
            return True
    
    return False

def funcBody(currentNodeLevel, astNode):
    if not skipErrors(first['funcBody'], follow['funcBody']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'funcBody', False)
    statementsNode = [AbstractSyntaxNode()]
    if   lookahead.tokenType  in first['funcBody']:
        if match(currentNodeLevel, '{') and statements(currentNodeLevel, statementsNode) and match(currentNodeLevel, '}'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([FuncBodyNode('funcBody')], [statementsNode[0]]))
            logDerivationRule("funcBody -> '{' statements '}'")
            writeOutput()
            return True
    
    return False

def statements(currentNodeLevel, astNode):
    if not skipErrors(first['statements'], follow['statements']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statements', False)
    statmentNode = [AbstractSyntaxNode()]
    if   lookahead.tokenType  in first['statements']:
        if statement(currentNodeLevel, statmentNode) and statements(currentNodeLevel, statmentNode):
            if not astNode[0].value:
                astNode[0] = statmentNode[0]
            else:
                astNode[0].addSibling(statmentNode[0])
            logDerivationRule("statements -> statement statements")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['statements']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("statements -> EPSILON")
        writeOutput()
        return True
    
    return False

def arrayDimenssion(currentNodeLevel, astNode):
    if not skipErrors(first['arrayDimenssion'], follow['arrayDimenssion']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arrayDimenssion', False)
    dimNode = [IntegerNode()]
    if lookahead.tokenType  in first['arrayDimenssion']:
        if arraySize(currentNodeLevel, dimNode) and arrayDimenssion(currentNodeLevel, dimNode):
            if not astNode[0].value:
                astNode[0] = (AbstractSyntaxNode.makeFamily([ArrayDimenssionNode('arrayDimenssions')], [dimNode[0]]))
            else:
                astNode[0].addSibling(dimNode[0])
            logDerivationRule("arrayDimenssion -> arraySize arrayDimenssion")
            writeOutput()
            return True
    elif  lookahead.tokenType  in follow['arrayDimenssion']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("arrayDimenssion -> EPSILON")
        writeOutput()
        return True
    
    return False

def statement(currentNodeLevel, astNode):
    if not skipErrors(first['statement'], follow['statement']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statement', False)
    typeNode = [TypeNode()]
    idNode = [IdNode()]
    dimNode = [ArrayDimenssionNode()]
    ifExprNode = [RelOpNode()]
    ifBlockNode = [ScopeBlockNode()]
    elseBlockNode = [ScopeBlockNode()]
    exprNode = [AbstractSyntaxNode()]
    relExprNode = [RelOpNode()]
    assignStatNode = [AssignNode()]
    forBlockNode = [ScopeBlockNode()]
    varNode = [VariableNode()]
    varAssignOrDeclNode = [AbstractSyntaxNode()]
    returnnode = [ReturnNode()]
    if   lookahead.tokenType  in first['statement']:
        if match(currentNodeLevel, 'int', typeNode) and match(currentNodeLevel, 'id', idNode) and arrayDimenssion(currentNodeLevel, dimNode) and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([VariableDeclNode('varDecl')], [typeNode[0], idNode[0], dimNode[0]]))
            logDerivationRule("statement -> 'int' 'id' arrayDimenssion ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'float', typeNode) and match(currentNodeLevel, 'id', idNode) and arrayDimenssion(currentNodeLevel, dimNode) and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([VariableDeclNode('varDecl')], [typeNode[0], idNode[0], dimNode[0]]))
            logDerivationRule("statement -> 'float' 'id' arrayDimenssion ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'if') and match(currentNodeLevel, '(') and expr(currentNodeLevel, ifExprNode) and match(currentNodeLevel, ')') and match(currentNodeLevel, 'then') and statBlock(currentNodeLevel, ifBlockNode) and match(currentNodeLevel, 'else') and statBlock(currentNodeLevel, elseBlockNode) and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([IfStatementNode('if')], [ifExprNode[0], ifBlockNode[0],elseBlockNode[0]]))
            logDerivationRule("statement -> 'if' '(' expr ')' 'then' statBlock 'else' statBlock ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'for') and match(currentNodeLevel, '(') and vType(currentNodeLevel, typeNode) and match(currentNodeLevel, 'id', idNode) and assignOp(currentNodeLevel) and expr(currentNodeLevel, exprNode) and match(currentNodeLevel, ';') and relExpr(currentNodeLevel, relExprNode) and match(currentNodeLevel, ';') and assignStat(currentNodeLevel, assignStatNode) and match(currentNodeLevel, ')') and statBlock(currentNodeLevel, forBlockNode) and match(currentNodeLevel, ';'):
            assignSideTree = AbstractSyntaxNode.makeFamily([AssignNode('assing')], [AbstractSyntaxNode.makeFamily([VariableDeclNode('var')], [typeNode[0], idNode[0]]), exprNode[0]])
            astNode[0] = (AbstractSyntaxNode.makeFamily([ForLoopNode('for')], [assignSideTree, relExprNode[0], assignStatNode[0], forBlockNode[0]]))
            logDerivationRule("statement -> 'for' '(' type 'id' assignOp expr ';' relExpr ';' assignStat ')' statBlock ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'get') and match(currentNodeLevel, '(') and variable(currentNodeLevel, varNode) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([GetNode('get')], [varNode[0]]))
            logDerivationRule("statement -> 'get' '(' variable ')' ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'put') and match(currentNodeLevel, '(') and expr(currentNodeLevel, exprNode) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([PutNode('put')], [exprNode[0]]))
            logDerivationRule("statement -> 'put' '(' expr ')' ';'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'return', returnnode) and match(currentNodeLevel, '(') and expr(currentNodeLevel, exprNode) and match(currentNodeLevel, ')') and match(currentNodeLevel, ';'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([returnnode[0]], [exprNode[0]]))
            logDerivationRule("statement -> 'return' '(' expr ')' ';'")
            writeOutput()
            return True
        elif varAssignOrDecl(currentNodeLevel, varAssignOrDeclNode):
            astNode[0] = (varAssignOrDeclNode[0])
            logDerivationRule("statement -> varAssignOrDecl")
            writeOutput()
            return True
    
    return False

def varAssignOrDecl(currentNodeLevel, astNode):
    if not skipErrors(first['varAssignOrDecl'], follow['varAssignOrDecl']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'varAssignOrDecl', False)
    idNode = [IdNode()]
    if lookahead.tokenType  in first['varAssignOrDecl']:
        if match(currentNodeLevel, 'id', idNode) and varAssignOrDeclTail(currentNodeLevel, idNode):
            astNode[0] = idNode[0]
            logDerivationRule("varAssignOrDecl -> 'id' varAssignOrDeclTail")
            writeOutput()
            return True
    parent = currentNodeLevel.parent
    parent.children.remove(currentNodeLevel)
    
    return False

def varAssignOrDeclTail(currentNodeLevel, astNode):
    if not skipErrors(first['varAssignOrDeclTail'], follow['varAssignOrDeclTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'varAssignOrDeclTail', False)
    idNode = [IdNode()]
    dimNode = [ArrayDimenssionNode()]
    indicesNode = [IndicesNode()]
    idnestNode = [AbstractSyntaxNode()]
    exprNode = [AbstractSyntaxNode()]
    if   lookahead.tokenType  in first['varAssignOrDeclTail']:
        if match(currentNodeLevel, 'id', idNode) and arrayDimenssion(currentNodeLevel, dimNode) and match(currentNodeLevel, ';'):
            firstId = [TypeNode()]
            firstId[0].setValue(astNode[0].value)
            astNode[0] = AbstractSyntaxNode.makeFamily([VariableDeclNode('varDecl')], [firstId[0], idNode[0], dimNode[0]])
            logDerivationRule("varAssignOrDeclTail -> 'id' arrayDimenssion ';'")
            writeOutput()
            return True
        elif indices(currentNodeLevel, indicesNode) and idnests(currentNodeLevel, idnestNode) and assignOp(currentNodeLevel) and expr(currentNodeLevel, exprNode) and match(currentNodeLevel, ';'):
            firstId = [AbstractSyntaxNode()]
            firstId[0] = (astNode[0])
            varNode = AbstractSyntaxNode.makeFamily([VariableNode('var')], [firstId[0], indicesNode[0], idnestNode[0]])
            astNode[0] = AbstractSyntaxNode.makeFamily([AssignNode('assign')], [varNode, exprNode[0]])
            logDerivationRule("varAssignOrDeclTail -> indices idnests assignOp expr ';'")
            writeOutput()
            return True
    
    return False

def assignStat(currentNodeLevel, astNode):
    if not skipErrors(first['assignStat'], follow['assignStat']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'assignStat', False)
    variableNode= [AbstractSyntaxNode()]
    exprNode = [AbstractSyntaxNode()]
    if lookahead.tokenType  in first['assignStat']:
        if variable(currentNodeLevel, variableNode) and assignOp(currentNodeLevel) and expr(currentNodeLevel, exprNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([AssignNode('assign')], [variableNode[0], exprNode[0]]))
            logDerivationRule("assignStat -> variable assignOp expr")
            writeOutput()
            return True
    
    return False

def statBlock(currentNodeLevel, astNode):
    if not skipErrors(first['statBlock'], follow['statBlock']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'statBlock', False)
    statementNode = [AbstractSyntaxNode()]
    if   lookahead.tokenType  in first['statBlock']:
        if match(currentNodeLevel, '{') and statements(currentNodeLevel, statementNode) and match(currentNodeLevel, '}'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([ScopeBlockNode('statBlock')], [statementNode[0]]))
            logDerivationRule("statBlock -> '{' statements '}'")
            writeOutput()
            return True
        elif statement(currentNodeLevel, statementNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([ScopeBlockNode('statBlock')], [statementNode[0]]))
            logDerivationRule("statBlock -> statement")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['statBlock']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("statBlock -> EPSILON")
        writeOutput()
        return True
    
    return False

def expr(currentNodeLevel, astNode):
    if not skipErrors(first['expr'], follow['expr']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'expr', False)
    arithExprNode = [ArithmExprNode()]
    if lookahead.tokenType  in first['expr']:
        if arithExpr(currentNodeLevel, arithExprNode) and exprTail(currentNodeLevel, arithExprNode):
            astNode[0] = arithExprNode[0]
            logDerivationRule("expr -> arithExpr exprTail")
            writeOutput()
            return True
    
    return False

def exprTail(currentNodeLevel, astNode):
    if not skipErrors(first['exprTail'], follow['exprTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'exprTail', False)
    relOpNode = [RelOpNode()]
    arithExprNode = [ArithmExprNode()]
    if lookahead.tokenType  in first['exprTail']:
        if relOp(currentNodeLevel, relOpNode) and arithExpr(currentNodeLevel, arithExprNode):
            oldastNode = [ArithmExprNode()]
            oldastNode[0] = (astNode[0])
            astNode[0] = AbstractSyntaxNode.makeFamily([relOpNode[0]], [oldastNode[0], arithExprNode[0]])
            logDerivationRule("exprTail -> relOp arithExpr")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['exprTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("exprTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def relExpr(currentNodeLevel, astNode):
    if not skipErrors(first['relExpr'], follow['relExpr']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'relExpr', False)
    arithExprNode = [ArithmExprNode()]
    arithExprNode2 = [ArithmExprNode()]
    relOpNode = [RelOpNode()]
    if   lookahead.tokenType  in first['relExpr']:
        if arithExpr(currentNodeLevel, arithExprNode) and relOp(currentNodeLevel, relOpNode) and arithExpr(currentNodeLevel, arithExprNode2):
            astNode[0] = (AbstractSyntaxNode.makeFamily([relOpNode[0]], [arithExprNode[0], arithExprNode2[0]]))
            logDerivationRule("relExpr -> arithExpr relOp arithExpr")
            writeOutput()
            return True
    
    return False

def arithExpr(currentNodeLevel, astNode):
    if not skipErrors(first['arithExpr'], follow['arithExpr']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arithExpr', False)
    termNode = [TermNode()]
    if lookahead.tokenType  in first['arithExpr']:
        if term(currentNodeLevel,termNode) and arithExprTail(currentNodeLevel, termNode):
            astNode[0] = termNode[0]
            logDerivationRule("arithExpr -> term relOp")
            writeOutput()
            return True
    
    return False

def arithExprTail(currentNodeLevel, astNode):
    if not skipErrors(first['arithExprTail'], follow['arithExprTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arithExprTail', False)
    addOpNode = [AddOpNode()]
    termNode = [TermNode()]
    if   lookahead.tokenType  in first['arithExprTail']:
        if addOp(currentNodeLevel,addOpNode) and term(currentNodeLevel, termNode) and arithExprTail(currentNodeLevel, termNode):
            idNode = [TermNode()]
            idNode[0] = (astNode[0])
            astNode[0] = AbstractSyntaxNode.makeFamily([addOpNode[0]], [idNode[0], termNode[0]])
            logDerivationRule("arithExprTail -> addOp term arithExprTail ")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['arithExprTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("arithExprTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def sign(currentNodeLevel, astNode):
    if not skipErrors(first['sign'], follow['sign']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'sign', False)
    if lookahead.tokenType in first['sign']:
        if match(currentNodeLevel, '+'):
            astNode[0] = (SignNode('+'))
            logDerivationRule("sign -> '+'")
            writeOutput()
            return True
        if match(currentNodeLevel, '-'):
            logDerivationRule("sign -> '-'")
            astNode[0] = (SignNode('-'))
            writeOutput()
            return True
    
    return False

def term(currentNodeLevel, astNode):
    if not skipErrors(first['term'], follow['term']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'term', False)
    factorNode = [FactorNode()]
    if lookahead.tokenType  in first['term']:
        if factor(currentNodeLevel, factorNode) and termTail(currentNodeLevel, factorNode):
            astNode[0] = factorNode[0]
            logDerivationRule("term -> factor termTail")
            writeOutput()
            return True
    
    return False

def termTail(currentNodeLevel, astNode):
    if not skipErrors(first['termTail'], follow['termTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'termTail', False)
    multOpNode = [MultOpNode()]
    factorNode = [FactorNode()]
    if lookahead.tokenType  in first['termTail']:
        if multOp(currentNodeLevel, multOpNode) and factor(currentNodeLevel, factorNode) and termTail(currentNodeLevel, factorNode):
            upTermNode = [FactorNode()]
            upTermNode[0] = (astNode[0])
            astNode[0] = AbstractSyntaxNode.makeFamily([multOpNode[0]], [upTermNode[0], factorNode[0]])
            logDerivationRule("termTail -> multOp factor termTail")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['termTail']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("termTail -> EPSILON")
        writeOutput()
        return True
    
    return False

def factor(currentNodeLevel, astNode):
    if not skipErrors(first['factor'], follow['factor']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'factor', False)
    varFuncNode = [AbstractSyntaxNode()]
    intNode = [IntegerNode()]
    floatNode = [FloatNode()]
    arithExprNode = [ArithmExprNode()]
    factorNode = [FactorNode()]
    signNode =[AbstractSyntaxNode()]
    if lookahead.tokenType  in first['factor']:
        if variableOrFuncCall(currentNodeLevel, varFuncNode):
            astNode[0] = (varFuncNode[0])
            logDerivationRule("factor -> variableOrFuncCall")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'intNum', intNode):
            astNode[0] = (intNode[0])
            logDerivationRule("factor -> intNum")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'floatNum', floatNode):
            astNode[0] = (floatNode[0])
            logDerivationRule("factor -> floatNum")
            writeOutput()
            return True
        elif match(currentNodeLevel, '(') and arithExpr(currentNodeLevel, arithExprNode) and match(currentNodeLevel, ')'):
            astNode[0] = (arithExprNode[0])
            logDerivationRule("factor -> '(' arithExpr ')'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'not') and factor(currentNodeLevel, factorNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([NotNode('not')], [factorNode[0]]))
            logDerivationRule("factor -> 'not' factor")
            writeOutput()
            return True
        elif sign(currentNodeLevel, signNode) and factor(currentNodeLevel, factorNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([signNode[0]], [factorNode[0]]))
            logDerivationRule("factor -> sign factor")
            writeOutput()
            return True
    
    return False

def variableOrFuncCall(currentNodeLevel, astNode):
    #if not skipErrors(first['variableOrFuncCall'], follow['variableOrFuncCall']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variableOrFuncCall', False)
    idNode = [IdNode()]
    nestNode = [AbstractSyntaxNode()]
    if lookahead.tokenType  in first['variableOrFuncCall']:
        if match(currentNodeLevel, 'id', idNode) and variableOrFuncCallTail(currentNodeLevel, idNode) and idnests(currentNodeLevel, nestNode):
            if nestNode[0].value:
                idNode[0].leftMostChild.addSibling(nestNode[0])
            astNode[0] = idNode[0]
            logDerivationRule("variableOrFuncCall -> 'id' variableOrFuncCallTail idnests")
            writeOutput()
            return True
    parent = currentNodeLevel.parent
    parent.children.remove(currentNodeLevel)
    #
    return False

def variableOrFuncCallTail(currentNodeLevel, astNode):
    #if not skipErrors(first['variableOrFuncCallTail'], follow['variableOrFuncCallTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variableOrFuncCallTail', False)
    idNode = [IdNode()]
    idNode[0] = (astNode[0])
    aParamsNode = [AParamsNode()]
    indicesNode = [IndicesNode()]
    if   lookahead.tokenType  in first['variableOrFuncCallTail']:
        if match(currentNodeLevel, '(') and aParams(currentNodeLevel, aParamsNode) and match(currentNodeLevel, ')'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([FCallNode('fCall')], [idNode[0], aParamsNode[0]]))
            logDerivationRule("variableOrFuncCallTail -> '(' aParams ')'")
            writeOutput()
            return True
        if indices(currentNodeLevel, indicesNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([VariableNode('variable')], [idNode[0], indicesNode[0]]))
            logDerivationRule("variableOrFuncCallTail -> indices")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['variableOrFuncCallTail']:
        astNode[0] = (AbstractSyntaxNode.makeFamily([VariableNode('variable')], [idNode[0]]))
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("variableOrFuncCallTail -> EPSILON")
        writeOutput()
        return True
    #
    return False

def variable(currentNodeLevel, astNode):
    if not skipErrors(first['variable'], follow['variable']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'variable', False)
    idNode = [IdNode()]
    indicesNode = [IndicesNode()]
    nestNode = [AbstractSyntaxNode()]
    if lookahead.tokenType  in first['variable']:
        if match(currentNodeLevel, 'id', idNode) and indices(currentNodeLevel, indicesNode) and idnests(currentNodeLevel, nestNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([VariableNode('var')], [idNode[0], indicesNode[0]]))
            if nestNode[0].value:
                astNode[0].leftMostChild.addSibling(nestNode[0])
            logDerivationRule("variable -> 'id' idnests indices")
            writeOutput()
            return True
    
    return False

def idnests(currentNodeLevel, astNode):
    if not skipErrors(first['idnests'], follow['idnests']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnests', False)
    nestNode = [AbstractSyntaxNode()]
    if lookahead.tokenType  in first['idnests']:
        if idnest(currentNodeLevel, nestNode) and idnests(currentNodeLevel, nestNode):
            if not astNode[0].value:
                astNode[0] = nestNode[0]
            else:
                astNode[0].leftMostChild.addSibling(nestNode[0])
            logDerivationRule("idnests -> idnest idnests")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['idnests']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("idnests -> EPSILON")
        writeOutput()
        return True
    
    return False

def indices(currentNodeLevel, astNode):
    #if not skipErrors(first['indices'], follow['indices']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'indices', False)
    indiceNode = [AbstractSyntaxNode()]
    if lookahead.tokenType  in first['indices']:
        if indice(currentNodeLevel, indiceNode) and indices(currentNodeLevel, indiceNode):
            if not astNode[0].value:
                astNode[0] = (AbstractSyntaxNode.makeFamily([IndicesNode('indices')], [indiceNode[0]]))
            else:
                astNode[0].addSibling(indiceNode[0])
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

def idnest(currentNodeLevel, astNode):
    if not skipErrors(first['idnest'], follow['idnest']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnest', False)
    idNode = [IdNode()]
    if lookahead.tokenType  in first['idnest']:
        if match(currentNodeLevel, '.') and match(currentNodeLevel, 'id', idNode) and idnestTail(currentNodeLevel, idNode):
            astNode[0] = (idNode[0])
            logDerivationRule("idnest -> '.' 'id' idnestTail")
            writeOutput()
            return True
    
    return False

def idnestTail(currentNodeLevel, astNode):
    if not skipErrors(first['idnestHeadTail'], follow['idnestHeadTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'idnestHeadTail', False)
    idNode = [IdNode()]
    idNode[0] = (astNode[0])
    aParamsNode = [AParamsNode()]
    indicesNode = [IndicesNode()]
    if   lookahead.tokenType  in first['idnestHeadTail']:
        if indices(currentNodeLevel, indicesNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([DataMemberNode('dataMember')], [idNode[0], indicesNode[0]]))
            logDerivationRule("idnestHeadTail -> indices")
            writeOutput()
            return True
        elif match(currentNodeLevel, '(') and aParams(currentNodeLevel, aParamsNode) and match(currentNodeLevel, ')'):
            astNode[0] = (AbstractSyntaxNode.makeFamily([FunctionMemberCallNode('fCall')], [idNode[0], aParamsNode[0]]))
            logDerivationRule("idnestTail -> '(' aParams ')'")
            writeOutput()
            return True
    elif  lookahead.tokenType  in follow['idnestHeadTail']:
        astNode[0] = (AbstractSyntaxNode.makeFamily([DataMemberNode('dataMember')], [astNode[0]]))
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("idnestTail -> EPSILON")
        writeOutput()
        return True
    return False

def indice(currentNodeLevel, astNode):
    if not skipErrors(first['indice'], follow['indice']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'indice', False)
    arithExprNode = [ArithmExprNode()]
    if   lookahead.tokenType  in first['indice']:
        if match(currentNodeLevel, '[') and arithExpr(currentNodeLevel, arithExprNode) and match(currentNodeLevel, ']'):
            astNode[0] = (arithExprNode[0])
            logDerivationRule("indice -> '[' arithExpr ']'")
            writeOutput()
            return True
    
    return False

def arraySize(currentNodeLevel, astNode):
    if not skipErrors(first['arraySize'], follow['arraySize']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'arraySize', False)
    numNode = [IntegerNode()]
    if lookahead.tokenType  in first['arraySize']:
        if match(currentNodeLevel, '[') and match(currentNodeLevel, 'intNum', numNode) and match(currentNodeLevel, ']'):
            astNode[0] = (numNode[0])
            logDerivationRule("arraySize -> '[' 'intNum' ']'")
            writeOutput()
            return True
    
    return False

def vType(currentNodeLevel, astNode):
    if not skipErrors(first['type'], follow['type']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'type', False)
    typeNode = [TypeNode()]
    if   lookahead.tokenType  in first['type']:
        if match(currentNodeLevel, 'int', typeNode):
            astNode[0] = typeNode[0]
            logDerivationRule("type -> 'int'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'float', typeNode):
            astNode[0] = typeNode[0]
            logDerivationRule("type -> 'float'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'id', typeNode):
            astNode[0] = typeNode[0]
            logDerivationRule("type -> 'id'")
            writeOutput()
            return True
    
    return False

def fParams(currentNodeLevel, astNode):
    if not skipErrors(first['fParams'], follow['fParams']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParams', False)
    astNode[0] = (FuncParamsNode('fparams'))
    typeNode = [TypeNode()]
    idNode = [IdNode()]
    dimNode = [ArrayDimenssionNode()]
    fParamsTailListNode = [FuncParamNode()]
    if lookahead.tokenType  in first['fParams']:
        if vType(currentNodeLevel, typeNode) and match(currentNodeLevel, 'id', idNode) and arrayDimenssion(currentNodeLevel, dimNode) and fParamsTailList(currentNodeLevel, fParamsTailListNode):
            fParamsNode = [FuncParamsNode()]
            fParamsNode[0] = (astNode[0])
            astNode[0] = (AbstractSyntaxNode.makeFamily([fParamsNode[0]], [AbstractSyntaxNode.makeFamily([FuncParamNode('param')], [typeNode[0], idNode[0], dimNode[0]]), fParamsTailListNode[0]]))
            logDerivationRule("fParams -> type 'id' arrayDimenssion fParamsTailList")
            writeOutput()
            return True
    elif lookahead.tokenType  in follow['fParams']:
        #astNode = FuncParamNode('param')
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("fParams -> EPSILON")
        writeOutput()
        return True
    
    return False

def aParams(currentNodeLevel, astNode):
    if not skipErrors(first['aParams'], follow['aParams']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParams', False)
    exprNode = [ExprNode()]
    listNode = [AbstractSyntaxNode()]
    if   lookahead.tokenType  in first['aParams']:
        if expr(currentNodeLevel, exprNode) and aParamsTailList(currentNodeLevel, listNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([AParamsNode('aParams')], [exprNode[0], listNode[0]]))
            logDerivationRule("aParams -> expr aParamsTailList")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['aParams']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("aParams -> EPSILON")
        writeOutput()
        return True
    
    return False

def fParamsTail(currentNodeLevel, astNode):
    if not skipErrors(first['fParamsTail'], follow['fParamsTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParamsTail', False)
    typeNode = [TypeNode()]
    idNode = [IdNode()]
    dimNode = [ArrayDimenssionNode()]
    if lookahead.tokenType  in first['fParamsTail']:
        if match(currentNodeLevel, ',') and vType(currentNodeLevel, typeNode) and match(currentNodeLevel, 'id', idNode) and arrayDimenssion(currentNodeLevel, dimNode):
            astNode[0] = (AbstractSyntaxNode.makeFamily([FuncParamNode('param')], [typeNode[0], idNode[0], dimNode[0]]))
            logDerivationRule("fParamsTail -> ',' type 'id' arrayDimenssion")
            writeOutput()
            return True
    
    return False

def aParamsTail(currentNodeLevel, astNode):
    if not skipErrors(first['aParamsTail'], follow['aParamsTail']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParamsTail', False)
    exprNode = [ExprNode()]
    if lookahead.tokenType  in first['aParamsTail']:
        if match(currentNodeLevel, ',') and expr(currentNodeLevel, exprNode):
            astNode[0] = (exprNode[0])
            logDerivationRule("aParamsTail -> ',' expr")
            writeOutput()
            return True
    
    return False

def fParamsTailList(currentNodeLevel, astNode):
    if not skipErrors(first['fParamsTailList'], follow['fParamsTailList']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'fParamsTailList', False)
    paramNode = [FuncParamNode()]
    if   lookahead.tokenType  in first['fParamsTailList']:
        if fParamsTail(currentNodeLevel, paramNode) and fParamsTailList(currentNodeLevel, paramNode):
            if not astNode[0].value:
                astNode[0] = (paramNode[0])
            else:
                astNode[0].addSibling(paramNode)
            logDerivationRule("fParamsTailList -> fParamsTail fParamsTailList")
            writeOutput()
            return True
    elif   lookahead.tokenType  in follow['fParamsTailList']:
        newTreeNode(currentNodeLevel, 'EPSILON', True)
        logDerivationRule("fParamsTailList -> EPSILON")
        writeOutput()
        return True
    
    return False

def aParamsTailList(currentNodeLevel, astNode):
    if not skipErrors(first['aParamsTailList'], follow['aParamsTailList']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'aParamsTailList', False)
    exprNode = [ExprNode()]
    if   lookahead.tokenType  in first['aParamsTailList']:
        if aParamsTail(currentNodeLevel, exprNode) and aParamsTailList(currentNodeLevel, exprNode):
            if not astNode[0].value:
                astNode[0] = (exprNode[0])
            else:
                astNode[0].addSibling(exprNode[0])
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
    if lookahead.tokenType  in first['assignOp']:
        if match(currentNodeLevel, '='):
            logDerivationRule("assignOp -> '='")
            writeOutput()
            return True
    
    return False

def relOp(currentNodeLevel, astNode):
    if not skipErrors(first['relOp'], follow['relOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'relOp', False)
    if lookahead.tokenType  in first['relOp']:
        if match(currentNodeLevel, 'eq', astNode):
            logDerivationRule("relOp -> 'eq'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'neq', astNode):
            logDerivationRule("relOp -> 'neq'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'lt', astNode):
            logDerivationRule("relOp -> 'lt'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'gt', astNode):
            logDerivationRule("relOp -> 'gt'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'leq', astNode):
            logDerivationRule("relOp -> 'leq'")
            writeOutput()
            return True
        elif match(currentNodeLevel, 'geq', astNode):
            logDerivationRule("relOp -> 'geq'")
            writeOutput()
            return True
    
    return False

def addOp(currentNodeLevel, astNode):
    if not skipErrors(first['addOp'], follow['addOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'addOp', False)
    if   lookahead.tokenType  in first['addOp']:
        if match(currentNodeLevel, '+', astNode):
            logDerivationRule("addOp -> '+'")
            writeOutput()
            return True
        if match(currentNodeLevel, '-', astNode):
            logDerivationRule("addOp -> '-'")
            writeOutput()
            return True
        if match(currentNodeLevel, 'or', astNode):
            logDerivationRule("addOp -> 'or'")
            writeOutput()
            return True
    
    return False

def multOp(currentNodeLevel, astNode):
    #if not skipErrors(first['multOp'], follow['multOp']): return False
    currentNodeLevel = newTreeNode(currentNodeLevel, 'multOp', False)
    if   lookahead.tokenType  in first['multOp']:
        if match(currentNodeLevel, '*', astNode):
            logDerivationRule("multOp -> '*'")
            writeOutput()
            return True
        if match(currentNodeLevel, '/', astNode):
            logDerivationRule("multOp -> '/'")
            writeOutput()
            return True
        if match(currentNodeLevel, 'and', astNode):
            logDerivationRule("multOp -> 'and'")
            writeOutput()
            return True
    return False
