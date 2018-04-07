from semantic.symbolTable.SymbolTable import *

class ConcreteSyntaxNode:

    def __init__(self, parent, value, isLeaf):
        self.parent = parent
        self.children = []
        self.value = value
        self.isLeaf = isLeaf

    def addChild(self, child):
        self.children.append(child)

    def __str__(self):
        return self.str('')

    def str(self, level):
        strNode = ''
        strNode += level + self.value + '\n'
        for child in self.children:
            strNode += child.str(level+'_')
        return strNode

class AbstractSyntaxNode:

    def __init__(self, value=None):
        self.value = value

        self.parent = None
        
        self.leftMostSibling = None
        self.rightSibling = None
        
        self.leftMostChild = None

        self.symbolTableEntry = None
        self.symTable = None

        self.nodeType = None

    def setValue(self, value):
        self.value = value

    def findScope(self, name):
        parent = self.parent
        while parent:
            if parent.symTable:
                entry = parent.symTable.search(name)
                if entry:
                    return entry
            parent = parent.parent

    def getScope(self):
        parent = self.parent
        while not parent.symTable:
            parent = parent.parent
        return parent.symTable

    def setNodeType(self, nodeType):
        self.nodeType = nodeType

    def createSymbolTable(self, tableName):
        self.symTable = SymbolTable(tableName)

    def addTableEntry(self, entry):
        self.symTable.addEntry(entry)

    def createSelfNodeEntry(self, entry):
        self.symbolTableEntry = entry

    def setEntryMemOffset(self, offset):
        self.symbolTableEntry.setOffset(offset)

    def setEntryMemSize(self, size):
        self.symbolTableEntry.setSize(size)

    def overwrite(self, other):
        self.value = other.value

        self.parent = other.parent

        self.leftMostSibling = other.leftMostSibling
        self.rightSibling = other.rightSibling

        self.leftMostChild = other.leftMostChild


    @staticmethod
    def makeFamily(op, children):
        children = list(filter(lambda child: child.value != None, children))
        if children and children[0]:
            node = children[0]
            for child in children[1:len(children)]:
                if child:
                    node.addSibling(child)
            op[0].adoptChildren(node)
        return op[0]

    def addSibling(self, siblingNode):
        node = self
        while node.rightSibling != None:
            node = node.rightSibling
        oldLeftMostSibling = None
        if not siblingNode.leftMostSibling:
            oldLeftMostSibling = siblingNode
        else:
            oldLeftMostSibling = siblingNode.leftMostSibling
        node.rightSibling =  oldLeftMostSibling
        if node.leftMostSibling:
            siblingNode.leftMostSibling =node.leftMostSibling
        else:
            siblingNode.leftMostSibling = node
        oldLeftMostSibling.parent = node.parent
        while oldLeftMostSibling.rightSibling != None:
            oldLeftMostSibling.rightSibling.leftMostSibling = oldLeftMostSibling.leftMostSibling
            oldLeftMostSibling.parent = node.parent
            oldLeftMostSibling = oldLeftMostSibling.rightSibling
    
    def adoptChildren(self, child):
        if self.leftMostChild != None:
            self.leftMostChild.addSibling(child)
        else:
            if child.leftMostSibling:
                child = child.leftMostSibling
            self.leftMostChild = child
            while child != None:
                child.setParent(self)
                child = child.rightSibling

    def setParent(self, parent):
        self.parent = parent

    def getChildrenList(self):
        children = []
        node = self.leftMostChild
        while node:
            children.append(node)
            node = node.rightSibling
        return children

    def accept(self, visitor, visitorHandlesAccept=False):
        if not visitorHandlesAccept:
            for child in self.getChildrenList():
                child.accept(visitor)
        visitor.visit(self)


    def __str__(self):
        return self.str('')

    def str(self, level):
        strNode = ''
        strNode += level + str(self.value) + ': '+self.__class__.__name__+'\n'
        if self.leftMostChild:
            strNode += self.leftMostChild.str(level+'\t')
        if self.rightSibling:
            strNode += self.rightSibling.str(level)
        return strNode

class ProgNode(AbstractSyntaxNode): pass
class ClassDeclNode(AbstractSyntaxNode): pass
class ClassSourceNode(AbstractSyntaxNode): pass
class ProgramNode(AbstractSyntaxNode): pass
class IdNode(AbstractSyntaxNode): pass
class TypeNode(AbstractSyntaxNode): pass
class InheritanceNode(AbstractSyntaxNode): pass
class ClassMemberDeclNode(AbstractSyntaxNode): pass
class ClassMethodNode(AbstractSyntaxNode): pass
class ClassAttributeNode(AbstractSyntaxNode): pass
class ArrayDimenssionNode(AbstractSyntaxNode): pass
class FuncParamsNode(AbstractSyntaxNode): pass
class FuncParamNode(AbstractSyntaxNode): pass
class FuncBodyNode(AbstractSyntaxNode): pass
class IntegerNode(AbstractSyntaxNode): pass
class FloatNode(AbstractSyntaxNode): pass
class AssignNode(AbstractSyntaxNode): pass
class VariableNode(AbstractSyntaxNode): pass
class VariableDeclNode(AbstractSyntaxNode): pass
class IfStatementNode(AbstractSyntaxNode): pass
class ForLoopNode(AbstractSyntaxNode): pass
class ReturnNode(AbstractSyntaxNode): pass
class PutNode(AbstractSyntaxNode): pass
class GetNode(AbstractSyntaxNode): pass
class AddOpNode(AbstractSyntaxNode): pass
class MultOpNode(AbstractSyntaxNode): pass
class RelOpNode(AbstractSyntaxNode): pass
class IndicesNode(AbstractSyntaxNode):pass
class ScopeBlockNode(AbstractSyntaxNode): pass
class ArithmExprNode(AbstractSyntaxNode): pass
class ExprNode(AbstractSyntaxNode): pass
class TermNode(AbstractSyntaxNode): pass
class FactorNode(AbstractSyntaxNode): pass
class AParamsNode(AbstractSyntaxNode): pass
class FunctionMemberCallNode(AbstractSyntaxNode):pass
class DataMemberNode(AbstractSyntaxNode): pass
class FCallNode(AbstractSyntaxNode): pass
class SignNode(AbstractSyntaxNode): pass
class NotNode(AbstractSyntaxNode): pass