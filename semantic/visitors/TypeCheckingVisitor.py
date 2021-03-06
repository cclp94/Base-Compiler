from semantic.visitors.Visitor import *
import re
from utils.ErrorLogger import ErrorLogger

class TypeCheckingVisitor(Visitor):
    varNameCounter = 0

    def __init__(self):
        pass

    @methdispatch
    def visit(self, node): pass
        #print('In main visit')

    @visit.register(ClassDeclNode)
    def _(self, node):
        supers = node.symTable.searchKind('inheritance')
        inheritanceList = []
        while supers:
            superClass = supers.pop()
            if not superClass.name.value in inheritanceList and superClass.name.value != node.leftMostChild.value.value:
                inheritanceList.append(superClass.name.value)
            else:
                ErrorLogger("Semantic Error: Circular Inheritance in class" +node.symTable.name.value)
                return
            supers = supers+ superClass.link.searchKind('inheritance')
        print(inheritanceList)

    @visit.register(InheritanceNode)
    def _(self, node):
        entry = node.symbolTableEntry
        superEntryScope = node.parent.findScope(entry.name.value)
        if not superEntryScope:
            ErrorLogger("Semantic Error at index " + str(
                node.symbolTableEntry.name.index) + ": Class not defined - " + entry.name.value)
            return
        entry.setLink(superEntryScope.link)
        print(entry)

    @visit.register(AParamsNode)
    def _(self, node):
        children = node.getChildrenList()
        func = node.parent
        scopeEntry = func.findScope(node.leftMostSibling.value.value)
        if not scopeEntry:
            ErrorLogger("Semantic Error at index " + node.leftMostSibling.value.index + ": Function not declared in scope.")
            return
        args = self.getFuncArgsFromTableType(scopeEntry.entryType)
        if len(args) != len(children):
            ErrorLogger("Semantic Error at index " +  str(node.leftMostSibling.value.index) + ": parameters passed do not represent the declared ones for function "+node.leftMostSibling.value.value+" : " + str(args))
            return
        for i in range(0,len(args)):
            if args[i] != children[i].nodeType:
                ErrorLogger("Semantic Error at index " + str(node.leftMostSibling.value.index) + ": parameters "+children[i].nodeType+" do not represent the declared ones : " + args[i])
                return

    def getFuncArgsFromTableType(self, entry):
        types = entry.partition(':')
        if len(types) > 2:
            args = list(filter(None, types[2].split(',')))
            return args

    @visit.register(FCallNode)
    def _(self, node):
        children = node.getChildrenList()
        name = children[0].value.value
        scopeEntry = node.findScope(name)
        if not scopeEntry:
            ErrorLogger("Semantic Error at index " + str(children[0].value.index) + ": Function " + name + "not defined")
            return
        funcType = self.getType(scopeEntry.entryType)
        node.setNodeType(funcType)
        # set moon tmp var entry
        moonTmpVar =  self.generateTempVarName()
        moonEntry = SymbolTableEntry(moonTmpVar, 'tempVar', funcType)
        node.createSelfNodeEntry(moonEntry)
        node.getScope().addEntry(moonEntry)

    @visit.register(ReturnNode)
    def _(self, node):
        #check return type
        actualReturnType = node.leftMostChild.nodeType
        expectedReturnType = node.findScope('returnType').entryType
        if actualReturnType == expectedReturnType:
            pass
        else:
            ErrorLogger("Semantic Error at index " + str(node.value.index) + ":"
                  " The value returned does not correspond to the"
                  " return type of the function " + node.parent.parent.symTable.name + " expected " + expectedReturnType)

    @visit.register(VariableNode)
    def _(self, node):
        if node.nodeType:
            return
        children = node.getChildrenList()
        idNode = children[0]
        scope = node.findScope(idNode.value.value)
        if not scope:
            ErrorLogger('Semantical Error at index '+ str(idNode.value.index) + ': variable ' + idNode.value.value + ' was not declared in the scope')
            return
        entryType = scope.entryType
        if len(children) > 1 and type(children[1]) is IndicesNode:
            indices = children[1].getChildrenList()
            entryTypeIndices = list(map(lambda x: re.sub('\]', '', x), entryType.split('[')))
            if len(entryTypeIndices) -1 == len(indices):
                entryType = entryTypeIndices[0]
            elif len(entryTypeIndices) -1 > len(indices):
                indiceDiff = len(entryTypeIndices) -1 - len(indices)
                diff = entryTypeIndices[0]
                for i in range(1+indiceDiff,len(entryTypeIndices)):
                    diff += entryTypeIndices[i]
                entryType = diff
            else:
                ErrorLogger("Semantic Error at index "+str(idNode.value.index)+": Array is not the same dimension as declared. At variable " + idNode.value.value)
        node.setNodeType(self.getType(entryType))


    @visit.register(DataMemberNode)
    @visit.register(FunctionMemberCallNode)
    def _(self, node):
        if node.nodeType:
            return
        # discover type by checking object's table
        stack = []
        #  go up until variable node
        parent = node
        while not type(parent) is VariableNode:
            #put parent name in stack
            stack.append(parent.leftMostChild)
            parent = parent.parent
        varEntry = parent.findScope(parent.leftMostChild.value.value)
        if not varEntry:
            ErrorLogger('Semantical Error at index '+ str(parent.leftMostChild.value.index) + ': variable ' + parent.leftMostChild.value.value + ' was not declared in the scope')
            return
        if self.isPrimitive(varEntry.entryType):
            ErrorLogger('Semantical Error at index ' + str(stack[-1].value.index) + ': ' + stack[-1].value.value + ' is not a member of ' + varEntry.entryType)
            return
        varEntry = parent.findScope(varEntry.entryType.partition('[')[0])
        for i in range(len(stack)-1, -1, -1):
            member = stack[i]
            if not varEntry.link:
                ErrorLogger('Semantical Error at index ' + str(member.value.index) + ': ' + member.value.value + ' is not a member of ' + varEntry.name.value)
                return
            entry = varEntry.link.search(member.value.value)
            if not entry:
                ErrorLogger('Semantical Error at index ' + str(member.value.index) + ': ' + member.value.value + ' is not a member of ' + varEntry.link.name.value)
                return
            else:
                varEntry = entry
        entryType = self.getType(varEntry.entryType)
        children = node.getChildrenList()
        if len(children) > 1 and type(children[1]) is IndicesNode:
            indices = children[1].getChildrenList()
            entryTypeIndices = list(map(lambda x: re.sub('\]', '', x), entryType.split('[')))
            if len(entryTypeIndices) -1 == len(indices):
                entryType = entryTypeIndices[0]
            elif len(entryTypeIndices) -1 > len(indices):
                indiceDiff = len(entryTypeIndices) -1 - len(indices)
                diff = entryTypeIndices[0]
                for i in range(1+indiceDiff,len(entryTypeIndices)):
                    diff += entryTypeIndices[i]
                entryType = diff
            else:
                ErrorLogger("Semantic Error: Array is not the same dimension as declared")

        parent.setNodeType(entryType)
        for memberNode in stack:
            memberNode.parent.setNodeType(entryType)
        node.setNodeType(entryType)
        if type(node) is FunctionMemberCallNode:
            # set moon tmp var entry
            moonTmpVar = self.generateTempVarName()
            moonEntry = SymbolTableEntry(moonTmpVar, 'tempVar', entryType)
            node.createSelfNodeEntry(moonEntry)
            node.getScope().addEntry(moonEntry)


    def isPrimitive(self, name):
        return bool(name.startswith('int') or name.startswith('float'))

    def getType(self, nodeType):
        return nodeType.partition(":")[0]#.partition('[')[0]

    @visit.register(AssignNode)
    def _(self, node):
        children = node.getChildrenList()
        lhsType = children[0].nodeType
        rhsType = children[1].nodeType
        if not lhsType:
            ErrorLogger("Semantic Error at index " + str(children[0].leftMostChild.value.index) + ": The left hand side of the assignment is undefined (" + str(children[0].leftMostChild.value.value) + ")")
            return
        if not rhsType:
            ErrorLogger("Semantic Error at index " + str(children[1].leftMostChild.value.index) + ": The right hand side of the assignment is undefined (" + str(children[1].leftMostChild.value.value) + ")")
            return
        if lhsType != rhsType:
            ErrorLogger("Semantic error at index " + str(children[0].leftMostChild.value.index) + ": "+lhsType+" cannot be assigned type (" + rhsType + ")")
        node.setNodeType(lhsType)

    @visit.register(AddOpNode)
    @visit.register(MultOpNode)
    @visit.register(RelOpNode)
    def _(self, node):
        children = node.getChildrenList()
        lhsType = children[0].nodeType
        rhsType = children[1].nodeType
        if not lhsType:
            ErrorLogger("Semantic Error at index " + str(node.value.index) + ": One of the operands in the expression is not defined (" + str(children[0].leftMostChild.value.value) + ")" )
            return
        if not rhsType:
            ErrorLogger("Semantic Error at index " + str(node.value.index) + ": One of the operands in the expression is not defined (" + str(children[1].leftMostChild.value.value) + ")")
            return
        if lhsType != rhsType:
            ErrorLogger("Semantic error at index " + str(node.value.index) + ": Operands must be of the same type. (" + lhsType + ") " + node.value.value + " (" + rhsType +  ")")
        node.setNodeType(lhsType)
        moonTmpVar = self.generateTempVarName()
        entry = SymbolTableEntry(moonTmpVar, 'tempVar', lhsType)
        node.createSelfNodeEntry(entry)
        node.getScope().addEntry(entry)

    def generateTempVarName(self):
        self.varNameCounter += 1
        return 'tmpVar'+str(self.varNameCounter)

    @visit.register(SignNode)
    @visit.register(NotNode)
    def _(self, node):
        child = node.leftMostChild
        node.setNodeType(child.nodeType)
        moonTmpVar = self.generateTempVarName()
        entry = SymbolTableEntry(moonTmpVar, 'tempVar', child.nodeType)
        node.createSelfNodeEntry(entry)
        node.getScope().addEntry(entry)

    @visit.register(VariableDeclNode)
    @visit.register(ClassAttributeNode)
    def _(self, node):
        children = node.getChildrenList()
        nodeType = node.leftMostChild.value.value
        if len(children) > 2:
            for dimension in children[2].getChildrenList():
                nodeType += '['+dimension.value.value+']'
        node.setNodeType(nodeType)
        if not self.isPrimitive(nodeType):
            node.symbolTableEntry.setLink(node.parent.findScope(nodeType.split('[')[0]).link)

    @visit.register(IntegerNode)
    def _(self, node):
        node.setNodeType('int')

    @visit.register(FloatNode)
    def _(self, node):
        node.setNodeType('float')

    @visit.register(ClassMethodNode)
    def _(self, node):
        params = node.getChildrenList()[2].getChildrenList()
        funcType = node.symbolTableEntry.entryType.split(':')[0]
        name = node.symbolTableEntry.name.value
        #find scope implementation
        scope = node.parent.getScope().search(name)
        #implementation params
        implParams = scope.link.searchKind('parameter')
        if len(params) != len(implParams):
            ErrorLogger("Semantic Error at index " + str(node.value.index) + ": Function "+name+" declares a different amount of parameters than it was declared")
        else:
            for i in range(len(params)):
                params[i].createSelfNodeEntry(implParams[i])

