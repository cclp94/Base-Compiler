from semantic.visitors.Visitor import *
import re
class CodeGenVisitor(Visitor):

    indent = '          '
    moonCode = ''
    outputLocation = ''
    registerPool = []
    stackRegister = ''
    frameRegister = ''
    uniqueTagCounter = 0
    globalOffset = 0

    def output(self):
        f = open(self.outputLocation, 'w')
        f.write(self.moonCode)

    def moonLine(self, tag, line, comment=None):
        if not line and comment:
            self.moonCode += self.indent + "%== "+str(comment)+" ==%\n"
        if line:
            if tag:
                self.moonCode += tag + self.indent[len(tag):]
            else:
                self.moonCode += self.indent
            self.moonCode += str(line)
            if comment:
                self.moonCode += "  % " + str(comment)
            self.moonCode += "\n"

    def initRegisters(self, size):
        for i in range(1, 15, 1):
            self.registerPool.append('R'+str(i))
        # stack register R13 and frame register is R14
        self.frameRegister = self.registerPool.pop()
        self.stackRegister = self.registerPool.pop()

    def __init__(self, outputLoc):
        self.outputLocation = outputLoc
        self.moonLine(None, None, "CODE FOR: " + outputLoc)
        self.initRegisters(15)

    def acceptChildren(self, node):
        for child in node.getChildrenList():
            child.accept(self, True)

    def moonTagGenerator(self):
        self.uniqueTagCounter += 1
        return 'f'+str(self.uniqueTagCounter)

    @methdispatch
    def visit(self, node): pass

    @visit.register(ProgNode)
    @visit.register(FuncBodyNode)
    @visit.register(IndicesNode)
    @visit.register(AParamsNode)
    def _(self, node):
        self.acceptChildren(node)

    @visit.register(ClassSourceNode)
    def _(self, node):
        node.symTable.setTag(self.moonTagGenerator())
        self.moonLine(node.symTable.tag, "sw 0("+self.stackRegister+"), "+self.frameRegister)
        self.acceptChildren(node)
        self.moonLine(None, "lw "+self.frameRegister+", 0("+self.stackRegister+")")
        self.moonLine(None, "jr "+self.frameRegister)

    @visit.register(ReturnNode)
    def _(self, node):
        self.acceptChildren(node)
        self.moonLine(None, "sw 4("+self.stackRegister+"), "+node.leftMostChild.moonRegister)
        self.registerPool.append(node.leftMostChild.moonRegister)
        node.leftMostChild.setMoonRegister(None)

    @visit.register(FCallNode)
    def _(self, node):
        registerToDeallocate =[]
        tmpReg = self.registerPool.pop()
        self.acceptChildren(node)
        funcScope = node.findScope(node.leftMostChild.value.value)
        funcOffset = -funcScope.size
        paramIndex = 1
        for param in node.getChildrenList()[1].getChildrenList():
            paramOffset = abs(-funcScope.link.entries[paramIndex].offset + node.getScope().offset +4)
            self.moonLine(None, "sw "+str(-paramOffset)+"("+self.stackRegister+"), "+ param.moonRegister, "Copy parameter")
            registerToDeallocate.append(param.moonRegister)
            param.setMoonRegister(None)
            paramIndex += 1
        self.moonLine(None, "addi "+self.stackRegister+", "+self.stackRegister+", "+ str(funcOffset-4))
        #jump to function
        self.moonLine(None, "jl "+self.frameRegister+", "+funcScope.link.tag)
        #put stack pointer back in place
        self.moonLine(None, "addi " + self.stackRegister + ", " + self.stackRegister + ", " + str(-funcOffset+4))
        #get return value
        self.moonLine(None, "addi "+tmpReg+", "+self.stackRegister+", "+str(funcOffset))
        self.moonLine(None, "lw "+ tmpReg + ", 0("+tmpReg+")")
        node.setMoonRegister(tmpReg)
        for reg in registerToDeallocate:
            self.registerPool.append(reg)

    @visit.register(ProgramNode)
    def _(self, node):
        self.moonLine(None, "entry", "program entry")
        self.moonLine(None, "align")
        self.moonLine(None, "addi "+self.stackRegister+", R0, topaddr", "init stack pointer register")
        self.moonLine(None, "addi " + self.frameRegister + ", R0, topaddr", "init frame pointer register")
        self.moonLine(None, "subi "+ self.stackRegister+", "+ self.stackRegister+", "+str(node.symTable.offset), "Set stack to top")
        self.acceptChildren(node)
        self.moonLine(None, "hlt", "program exit")
        self.moonLine(None, None, "END OF PROGRAM")
        #self.moonLine("buf", "res 20", "mem for moon lib subroutines")
        print(self.moonCode)
        if len(self.registerPool) < 12:
            print("Register not deallocated", self.registerPool)

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

    @visit.register(AssignNode)
    def _(self, node):
        children = node.getChildrenList()
        registersToDealloc = []
        lhs = node.findScope(children[0].leftMostChild.value.value)
        lhsOffset = lhs.offset
        # Right hand side
        children[1].accept(self, True)
        tmpReg = self.registerPool.pop()
        if len(children[0].getChildrenList()) > 1:
            self.acceptChildren(children[0])
            indicesChildren = children[0].getChildrenList()[1].getChildrenList()
            indices = list(map(lambda x: re.sub('\]', '', x), lhs.entryType.split('[')))
            self.moonLine(None, "addi " + tmpReg + ", R0, 0")
            for i in range(len(indicesChildren)):
                counter = 1
                for index in indices[2+i:]:
                    counter *= int(index)
                self.moonLine(None, "muli "+indicesChildren[i].moonRegister+", "+indicesChildren[i].moonRegister+", "+str(-counter*self.typeSizeOf(node, indices[0])))
                self.moonLine(None, "add " + tmpReg + ", " + tmpReg + ", " + indicesChildren[i].moonRegister)
                #return index register
                registersToDealloc.append(indicesChildren[i].moonRegister)
            self.moonLine(None, "addi " + tmpReg + ", " + tmpReg + ", " + str(-1*self.typeSizeOf(node, indices[0])))
            self.moonLine(None, "subi " + tmpReg + ", " + tmpReg + ", " + str(lhsOffset+self.globalOffset))
            self.moonLine(None,"add " + tmpReg + ", " + self.stackRegister + ", " + tmpReg)
        else:
            self.moonLine(None, "addi "+tmpReg+", "+self.stackRegister+", "+str(lhsOffset+self.globalOffset))
        # Assign to register
        self.moonLine(None, "sw 0("+tmpReg+"), "+children[1].moonRegister)
        self.registerPool.append(tmpReg)
        self.registerPool.append(children[1].moonRegister)
        children[1].setMoonRegister(None)
        for reg in registersToDealloc:
            self.registerPool.append(reg)

    @visit.register(AddOpNode)
    def _(self, node):
        children = node.getChildrenList()
        if type(children[1]) is FCallNode:
            children[1].accept(self, True)
            children[0].accept(self, True)
        else:
            children[0].accept(self, True)
            children[1].accept(self, True)
        node.setMoonRegister(self.registerPool.pop())
        op = ''
        if node.value.value == '+':
            op = 'add '
        elif node.value.value == '-':
            op = 'sub '
        elif node.value.value == 'or':
            op = 'or '
        self.moonLine(None,op + node.moonRegister + ", " + children[0].moonRegister + ", " + children[1].moonRegister)
        self.registerPool.append(children[0].moonRegister)
        self.registerPool.append(children[1].moonRegister)
        children[0].setMoonRegister(None)
        children[1].setMoonRegister(None)

    @visit.register(MultOpNode)
    def _(self, node):
        children = node.getChildrenList()
        if type(children[1]) is FCallNode:
            children[1].accept(self, True)
            children[0].accept(self, True)
        else:
            children[0].accept(self, True)
            children[1].accept(self, True)

        children = node.getChildrenList()
        node.setMoonRegister(self.registerPool.pop())
        op = ''
        if node.value.value == '*':
            op = 'mul '
        elif node.value.value == '/':
            op = 'sub '
        elif node.value.value == 'and':
            op = 'and '
        self.moonLine(None, op + node.moonRegister + ", " + children[0].moonRegister + ", " + children[1].moonRegister)
        self.registerPool.append(children[0].moonRegister)
        self.registerPool.append(children[1].moonRegister)
        children[0].setMoonRegister(None)
        children[1].setMoonRegister(None)

    @visit.register(IntegerNode)
    def _(self, node):
        num = node.value.value
        reg = self.registerPool.pop()
        # Assign to register
        self.moonLine(None, "addi " + reg + ", R0, " + num)
        node.setMoonRegister(reg)

    @visit.register(VariableNode)
    def _(self, node):
        children = node.getChildrenList()
        var = node.findScope(children[0].value.value)
        if len(children) > 1:
            tmpReg = self.registerPool.pop()
            node.setMoonRegister(tmpReg)
            self.acceptChildren(children[1])
            indicesChildren = children[1].getChildrenList()
            indices = list(map(lambda x: re.sub('\]', '', x), var.entryType.split('[')))
            self.moonLine(None, "addi " + tmpReg + ", R0, 0")
            for i in range(len(indicesChildren)):
                counter = 1
                for index in indices[2 + i:]:
                    counter *= int(index)
                self.moonLine(None, "muli " + indicesChildren[i].moonRegister + ", " + indicesChildren[
                    i].moonRegister + ", " + str(-counter * self.typeSizeOf(node, indices[0])))
                self.moonLine(None, "add " + tmpReg + ", " + tmpReg + ", " + indicesChildren[i].moonRegister)
                # return index register
                self.registerPool.append(indicesChildren[i].moonRegister)
            self.moonLine(None, "addi " + tmpReg + ", " + tmpReg + ", " + str(-1*self.typeSizeOf(node, indices[0])))
            self.moonLine(None, "subi " + tmpReg + ", " + tmpReg + ", " + str(var.offset+self.globalOffset))
            self.moonLine(None, "add " + tmpReg + ", " + self.stackRegister + ", " + tmpReg)
            self.moonLine(None, "lw " + node.moonRegister + ", 0(" + node.moonRegister + ")")
        else:
            varOffset = var.offset+self.globalOffset
            node.setMoonRegister(self.registerPool.pop())
            self.moonLine(None, "lw " + node.moonRegister + ", " + str(varOffset) + "(" + self.stackRegister + ")")

    @visit.register(ScopeBlockNode)
    def _(self, node):
        self.moonLine(node.symTable.tag, "nop")
        # temp scope, stack move
        if node.symTable.offset > 0:
            self.moonLine(None, "subi "+self.stackRegister+", "+self.stackRegister+", "+str(node.symTable.offset), "Alloc stack for temp scope")
            self.globalOffset += node.symTable.offset
        self.acceptChildren(node)
        if node.symTable.offset > 0:
            # end of temp scope, move stack back
            self.globalOffset -= node.symTable.offset
            self.moonLine(None, "addi " + self.stackRegister + ", " + self.stackRegister + ", " + str(node.symTable.offset),"Dealloc stack for temp scope")

    @visit.register(IfStatementNode)
    def _(self, node):
        print(node)
        children = node.getChildrenList()
        children[0].accept(self, True)
        ifTag = self.moonTagGenerator()
        elseTag = self.moonTagGenerator()
        endIfTag = self.moonTagGenerator()
        self.moonLine(None, "bz "+children[0].moonRegister+", "+elseTag,  "If Statement")
        children[1].symTable.setTag(ifTag)
        children[1].accept(self, True)
        self.moonLine(None, "j "+ endIfTag)
        children[2].symTable.setTag(elseTag)
        children[2].accept(self, True)
        self.moonLine(endIfTag, "nop", "If statement end")
        self.registerPool.append(children[0].moonRegister)
        children[0].setMoonRegister(None)


    @visit.register(RelOpNode)
    def _(self, node):
        self.acceptChildren(node)
        tmpReg = self.registerPool.pop()
        children = node.getChildrenList()
        op = ''
        if node.value.tokenType == 'leq':
            op = 'cle'
        elif node.value.tokenType == 'eq':
            op = 'ceq'
        elif node.value.tokenType == 'neq':
            op = 'cne'
        elif node.value.tokenType == 'lt':
            op = 'clt'
        elif node.value.tokenType == 'gt':
            op = 'cgt'
        elif node.value.tokenType == 'geq':
            op = 'cge'
        self.moonLine(None, op+" "+tmpReg+", "+children[0].moonRegister+", "+ children[1].moonRegister)
        self.registerPool.append(children[0].moonRegister)
        self.registerPool.append(children[1].moonRegister)
        children[0].setMoonRegister(None)
        children[1].setMoonRegister(None)
        node.setMoonRegister(tmpReg)

    @visit.register(PutNode)
    def _(self, node):
        self.acceptChildren(node)
        child = node.leftMostChild
        self.moonLine(None, "putc "+child.moonRegister)
        self.registerPool.append(child.moonRegister)
        child.setMoonRegister(None)

