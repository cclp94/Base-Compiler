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

    @visit.register(ClassDeclNode)
    @visit.register(ProgramNode)
    def _(self, node):
        children = node.symTable.entries
        frameOffset = 0
        for child in children:
            child.setOffset(frameOffset)
            frameOffset += child.size
        node.symTable.setOffset(frameOffset)
        if node.symbolTableEntry:
            node.setEntryMemSize(frameOffset)
        print(node.symTable)

    @visit.register(ScopeBlockNode)
    def _(self, node):
        children = node.symTable.entries
        frameOffset = 0
        for child in children:
            child.setOffset(frameOffset-child.size)
            frameOffset -= child.size
        node.symTable.setOffset(-frameOffset)
        if node.symbolTableEntry:
            node.setEntryMemSize(-frameOffset)
        print(node.symTable)

    @visit.register(IfStatementNode)
    def _(self, node):
        children = node.symTable.entries
        frameOffset = 0
        children[0].setOffset(frameOffset)
        frameOffset += children[0].size
        children[1].setOffset(frameOffset)
        frameOffset += children[1].size
        tmpVarOffset = -children[2].size
        for tmp in children[2:]:
            tmp.setOffset(tmpVarOffset-tmp.size)
            tmpVarOffset -= tmp.size
        node.symTable.setOffset(frameOffset)
        if node.symbolTableEntry:
            node.setEntryMemSize(0)
        print(node.symTable)

    @visit.register(ForLoopNode)
    def _(self, node):
        children = node.symTable.entries
        frameOffset = 0
        for child in children:
            child.setOffset(frameOffset-child.size)
            frameOffset -= child.size
        node.symTable.setOffset(frameOffset)
        if node.symbolTableEntry:
            node.setEntryMemSize(0)
        print(node.symTable)

    @visit.register(ClassMethodNode)
    def _(self, node):
        node.setEntryMemSize(0)

    @visit.register(ClassSourceNode)
    def _(self, node):
        children = node.symTable.entries
        # reserve memory for  return address
        frameOffset = 4
        for child in children:
            if not child.size and child.size != 0:
                child.setSize(self.typeSizeOf(node, child.entryType))
            child.setOffset(frameOffset)
            frameOffset += child.size
        node.symTable.setOffset(frameOffset-4)
        if node.symbolTableEntry:
            node.setEntryMemSize(frameOffset-4)
        print(node.symTable)

    @visit.register(ClassAttributeNode)
    @visit.register(VariableDeclNode)
    @visit.register(FuncParamNode)
    @visit.register(InheritanceNode)
    @visit.register(AddOpNode)
    @visit.register(MultOpNode)
    @visit.register(RelOpNode)
    @visit.register(NotNode)
    @visit.register(FCallNode)
    @visit.register(FunctionMemberCallNode)
    def _(self, node):
        size = self.typeSizeOf(node)
        node.setEntryMemSize(size)