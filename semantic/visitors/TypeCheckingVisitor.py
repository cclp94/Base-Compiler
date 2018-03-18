from semantic.visitors.Visitor import *

class TypeCheckingVisitor(Visitor):

    def __init__(self):
        pass

    @methdispatch
    def visit(self, node): pass
        #print('In main visit')

    @visit.register(ReturnNode)
    def _(self, node):
        #check return type
        actualReturnType = node.leftMostChild.nodeType
        expectedReturnType = node.parent.parent.symTable.search('returnType').entryType
        if actualReturnType == expectedReturnType:
            pass
        else:
            print("Semantic Error at index " + str(node.value.index) + ":"
                  " The value returned does not correspond to the"
                  " return type of the function " + node.parent.parent.symTable.name + " expected " + expectedReturnType)

    @visit.register(DataMemberNode)
    def _(self, node):
        # discover type by checking object's table
        stack = []
        #  go up until variable node
        parent = node.parent
        while not type(parent) is VariableNode:
            #put parent name in stack
            stack.append(parent.leftMostChild.value)
            parent = parent.parent
        varEntry = parent.findScope(parent.leftMostChild.value.value)
        if not varEntry:
            print('Semantical Error at index '+ parent.leftMostChild.value.index + ': variable ' + parent.leftMostChild.value.value + ' was not declared in the scope')
        while len(stack) > 0:
            member = stack.pop()
            if not varEntry.link:
                print('Semantical Error at index ' + str(member.index) + ': ' + member.value + ' is not a member of ' + varEntry.name.value)
                return
            entry = varEntry.link.search(member.value)
            if not entry:
                print('Semantical Error at index ' + str(member.index) + ': ' + member.value + ' is not a member of ' + varEntry.link.name)
                return
            else:
                varEntry = entry
        node.setNodeType(varEntry.entryType)


    @visit.register(VariableDeclNode)
    @visit.register(ClassAttributeNode)
    def _(self, node):
        children = node.getChildrenList()
        nodeType = node.leftMostChild.value.value
        if len(children) > 2:
            for dimension in children[2].getChildrenList():
                nodeType += '['+dimension.value.value+']'
        node.setNodeType(nodeType)

    @visit.register(IntegerNode)
    def _(self, node):
        node.setNodeType('int')

    @visit.register(FloatNode)
    def _(self, node):
        node.setNodeType('float')