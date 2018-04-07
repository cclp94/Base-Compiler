from semantic.visitors.Visitor import *
import re

class MemAllocationVisitor(Visitor):

    stackMem = 1
    frameMem = 0

    def typeSizeOf(self, node, type=None):
        if not type:
            val = node.symbolTableEntry.entryType
        else:
            val = type
        entryTypeIndices = list(map(lambda x: re.sub('\]', '', x), val.split('[')))
        size = 0
        if entryTypeIndices[0] == 'int':
            size = 4
        elif entryTypeIndices[0] == 'float':
            size = 8
        else:
            scope = node.findScope(entryTypeIndices[0]).link
            size = abs(scope.offset)
        for index in entryTypeIndices[1:]:
            size *= int(index)
        return size


    def __init__(self):
        pass

    @methdispatch
    def visit(self, node): pass

    # @visit.register(ProgNode)
    # def _(self, node):
    #     node.createSymbolTable('global')
    #     children = node.getChildrenList()
    #     for child in children:
    #         if child.symbolTableEntry:
    #             node.addTableEntry(child.symbolTableEntry)
    #     print(node.symTable)

    @visit.register(ProgNode)
    @visit.register(ClassDeclNode)
    @visit.register(ProgramNode)
    def _(self, node):
        children = node.symTable.entries
        frameOffset = 0
        for child in children:
            child.setOffset(frameOffset-child.size)
            frameOffset -= child.size
        node.symTable.setOffset(frameOffset)
        if node.symbolTableEntry:
            node.setEntryMemSize(-frameOffset)
        print(node.symTable)

    @visit.register(ClassSourceNode)
    def _(self, node):
        children = node.symTable.entries
        # reserve memory for  return address
        frameOffset = -4
        for child in children:
            if not child.size:
                child.setSize(self.typeSizeOf(node, child.entryType))
            child.setOffset(frameOffset - child.size)
            frameOffset -= child.size
        node.symTable.setOffset(frameOffset)
        if node.symbolTableEntry:
            node.setEntryMemSize(-frameOffset)
        print(node.symTable)

    @visit.register(ClassAttributeNode)
    @visit.register(VariableDeclNode)
    @visit.register(FuncParamNode)
    @visit.register(InheritanceNode)
    def _(self, node):
        size = self.typeSizeOf(node)
        node.setEntryMemSize(size)

    # @visit.register(ClassMethodNode)
    # def _(self, node):
    #     children = node.getChildrenList()
    #     id = children[1].value
    #     methodReturnAndParms = children[0].value.value + ':'
    #     params = children[2].getChildrenList()
    #     if params:
    #         for param in params:
    #             paramChildren = param.getChildrenList()
    #             paramType = paramChildren[0].value.value
    #             if len(paramChildren) == 3:
    #                 for dimension in paramChildren[2].getChildrenList():
    #                     paramType += '[' + str(dimension.value.value) + ']'
    #             paramType += ','
    #             methodReturnAndParms += paramType
    #     entry = SymbolTableEntry(id, 'function', methodReturnAndParms)
    #     node.createSelfNodeEntry(entry)

    # @visit.register(ClassSourceNode)
    # def _(self, node):
    #     children = node.getChildrenList()
    #     returnType = children[0].value.value
    #     id1 = children[1]
    #     id2 = children[2]
    #     name = ''
    #     # check namespace for linking table to definition
    #     namespace = None
    #     if id2.value:
    #         name = id2.value
    #         namespace = id1.value.value
    #     else:
    #         name = id1.value
    #     params = children[3]
    #     node.createSymbolTable(name.value)
    #     #add return entry
    #     node.addTableEntry(SymbolTableEntry('returnType', 'returnType', returnType))
    #     paramsList = ''
    #     for param in params.getChildrenList():
    #         paramChildren = param.getChildrenList()
    #         paramType = paramChildren[0].value.value
    #         if len(paramChildren) == 3:
    #             for dimension in paramChildren[2].getChildrenList():
    #                 paramType += '[' + str(dimension.value.value) + ']'
    #         paramsList += paramType
    #         paramsList += ','
    #         node.addTableEntry(SymbolTableEntry(paramChildren[1].value, 'parameter', paramType))
    #     body = children[4]
    #     bodyChildren = body.getChildrenList()
    #     for child in bodyChildren:
    #         if child.symbolTableEntry:
    #             node.addTableEntry(child.symbolTableEntry)
    #     # add to class if namespace is defined
    #     if namespace:
    #         node.createSelfNodeEntry(SymbolTableEntry(name, 'classMemberFunction:'+namespace, returnType+':'+paramsList, node.symTable))
    #     else:
    #         node.createSelfNodeEntry(SymbolTableEntry(name, 'function', returnType+':'+paramsList, node.symTable))
    #     print(node.symTable)

    # @visit.register(ProgramNode)
    # def _(self, node):
    #     node.createSymbolTable('program')
    #     bodyChildren = node.leftMostChild.getChildrenList()
    #     for child in bodyChildren:
    #         if child.symbolTableEntry:
    #             node.addTableEntry(child.symbolTableEntry)
    #     node.createSelfNodeEntry(SymbolTableEntry('program', 'mainFunction', None, node.symTable))
    #     print(node.symTable)

    # @visit.register(VariableDeclNode)
    # def _(self, node):
    #     children = node.getChildrenList()
    #     id = children[1].value
    #     varType = children[0].value.value
    #     if len(children) == 3:
    #         for dimension in children[2].getChildrenList():
    #             varType += '[' + str(dimension.value.value) + ']'
    #     entry = SymbolTableEntry(id, 'variable', varType)
    #     node.createSelfNodeEntry(entry)

    # @visit.register(InheritanceNode)
    # def _(self, node):
    #     entry = SymbolTableEntry(node.value, 'inheritance', None)
    #     node.createSelfNodeEntry(entry)

    # @visit.register(ForLoopNode)
    # def _(self, node):
    #     node.createSymbolTable('forLoop')
    #     children = node.getChildrenList()
    #     assignStat = children[0]
    #     if assignStat.leftMostChild.symbolTableEntry:
    #         node.addTableEntry(assignStat.leftMostChild.symbolTableEntry)
    #     if children[3].symbolTableEntry:
    #         node.addTableEntry(children[3].symbolTableEntry)
    #     node.createSelfNodeEntry(SymbolTableEntry('forLoop', 'forLoop', None, node.symTable))
    #     print(node.symTable)

    # @visit.register(IfStatementNode)
    # def _(self, node):
    #     node.createSymbolTable('ifStatement')
    #     children = node.getChildrenList()
    #     for child in children:
    #         if child.symbolTableEntry:
    #             node.addTableEntry(child.symbolTableEntry)
    #     node.createSelfNodeEntry(SymbolTableEntry('ifStatement', 'ifStatement', None, node.symTable))
    #     print(node.symTable)

    # @visit.register(ScopeBlockNode)
    # def _(self, node):
    #     node.createSymbolTable('anonymous')
    #     children = node.getChildrenList()
    #     for child in children:
    #         if child.symbolTableEntry:
    #             node.addTableEntry(child.symbolTableEntry)
    #     node.createSelfNodeEntry(SymbolTableEntry('statBlockScope', 'statBlockScope', None, node.symTable))
    #     print(node.symTable)