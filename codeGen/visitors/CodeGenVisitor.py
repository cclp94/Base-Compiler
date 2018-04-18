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

    def loadValFromNodeOffset(self, nodeOffset, registerDest):
        if type(nodeOffset) is int:
            self.moonLine(None, "lw " + registerDest + ", " + str(nodeOffset) + "(" + self.stackRegister + ")")
        else:
            #it is a register loc
            self.moonLine(None, "add " + registerDest + ", " + self.stackRegister + ", " + nodeOffset)
            self.moonLine(None, "lw " + registerDest + ", 0(" + registerDest + ")")
            self.registerPool.append(nodeOffset)
        return registerDest

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
        for i in range(1, 13, 1):
            self.registerPool.append('R'+str(i))
        # stack register R13 and frame register is R14
        self.frameRegister = 'R15'
        self.stackRegister = 'R14'

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
        tmpReg = self.registerPool.pop()
        if not type(node.leftMostChild) is IntegerNode:
            tmpReg = self.loadValFromNodeOffset(node.leftMostChild.moonStackOffset, tmpReg)
        else:
            self.moonLine(None, "addi "+tmpReg+", R0, "+str(node.leftMostChild.moonStackOffset))
        self.moonLine(None, "sw "+str(4+self.globalOffset)+"("+self.stackRegister+"), "+tmpReg)
        self.registerPool.append(tmpReg)
        node.leftMostChild.setMoonRegister(None)

    @visit.register(FCallNode)
    @visit.register(FunctionMemberCallNode)
    def _(self, node):
        registerToDeallocate =[]
        self.acceptChildren(node)
        funcScope = node.getGlobalScope().search(node.leftMostChild.value.value)
        funcOffset = -funcScope.size
        fparams = node.getChildrenList()
        if len(fparams) > 1:
            paramIndex = 1
            for param in node.getChildrenList()[1].getChildrenList():
                paramOffset = abs(-funcScope.link.entries[paramIndex].offset + node.getGlobalScope().search(node.leftMostChild.value.value).link.offset +4)
                paramRegister = self.registerPool.pop()
                if not type(param) is IntegerNode:
                    paramRegister = self.loadValFromNodeOffset(param.moonStackOffset, paramRegister)
                else:
                    self.moonLine(None, "addi "+paramRegister+", R0, " + str(param.moonStackOffset))
                self.moonLine(None, "sw "+str(-paramOffset)+"("+self.stackRegister+"), "+ paramRegister, "Copy parameter")
                registerToDeallocate.append(paramRegister)
                param.setMoonRegister(None)
                paramIndex += 1
        self.moonLine(None, "addi "+self.stackRegister+", "+self.stackRegister+", "+ str(funcOffset-4))
        #jump to function
        self.moonLine(None, "jl "+self.frameRegister+", "+funcScope.link.tag)
        #put stack pointer back in place
        self.moonLine(None, "addi " + self.stackRegister + ", " + self.stackRegister + ", " + str(-funcOffset+4))
        #get return value
        node.setMoonStackOffset(node.symbolTableEntry.offset+self.globalOffset)
        tmpReg = self.registerPool.pop()
        self.moonLine(None, "lw "+tmpReg+", "+str(funcOffset)+"("+self.stackRegister+")")
        self.moonLine(None, "sw "+str(node.moonStackOffset)+"("+self.stackRegister+"), "+tmpReg)
        self.registerPool.append(tmpReg)
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
        self.moonLine("buf", "res 20", "mem for moon lib subroutines")
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
        lhs = node.findScope(children[0].leftMostChild.value.value)
        lhsOffset = lhs.offset
        # Right hand side
        children[1].accept(self, True)
        children[0].accept(self, True)
        # Assign to register
        #load rhs
        rhsRegister = self.registerPool.pop()
        if not type(children[1]) is IntegerNode:
            rhsRegister = self.loadValFromNodeOffset(children[1].moonStackOffset, rhsRegister)
        else:
            self.moonLine(None, "addi " + rhsRegister + ", R0, " + str(children[1].moonStackOffset))
        #lhs register
        if type(children[0].moonStackOffset) is int:
            self.moonLine(None, "sw "+str(children[0].moonStackOffset)+"("+self.stackRegister+"), "+rhsRegister)
        else:
            lhsRegister = self.registerPool.pop()
            self.moonLine(None, "add "+lhsRegister+", "+self.stackRegister+", "+children[0].moonStackOffset)
            self.registerPool.append(children[0].moonStackOffset)
            self.moonLine(None,"sw 0(" + lhsRegister + "), " + rhsRegister)
            self.registerPool.append(lhsRegister)
        self.registerPool.append(rhsRegister)
        children[1].setMoonRegister(None)
        children[0].setMoonRegister(None)

    @visit.register(DataMemberNode)
    def _(self, node):
        children = node.getChildrenList()
        if len(children) > 1:
            self.acceptChildren(node)
            if type(children[1]) is IndicesNode:
                varNode = node.parent
                varEntry = node.findScope(varNode.leftMostChild.value.value)
                dataEntry = varEntry.link.search(node.leftMostChild.value.value)
                tmpReg = self.registerPool.pop()
                #self.acceptChildren(children[1])
                indicesChildren = children[1].getChildrenList()
                indices = list(map(lambda x: re.sub('\]', '', x), dataEntry.entryType.split('[')))
                self.moonLine(None, "addi " + tmpReg + ", R0, 0")
                for i in range(len(indicesChildren)):
                    counter = 1
                    for index in indices[2 + i:]:
                        counter *= int(index)
                    # Load index
                    indexReg = self.registerPool.pop()
                    if type(indicesChildren[i]) is IntegerNode:
                        self.moonLine(None, "addi "+indexReg+", R0, "+str(indicesChildren[i].moonStackOffset))
                    else:
                        self.moonLine(None, "lw "+indexReg+", "+str(indicesChildren[i].moonStackOffset)+"("+self.stackRegister+")")
                    self.moonLine(None, "muli " + indexReg + ", " + indexReg + ", " + str(counter))
                    self.moonLine(None, "add " + tmpReg + ", " + tmpReg + ", " + indexReg)
                    # return index register
                    self.registerPool.append(indexReg)
                self.moonLine(None, "addi " + tmpReg + ", " + tmpReg + ", 1")
                self.moonLine(None,"muli " + tmpReg + ", " + tmpReg + ", " + str(int(self.typeSizeOf(node, indices[0])/2)))
                self.moonLine(None, "addi " + tmpReg + ", " + tmpReg + ", " + str(dataEntry.offset+self.globalOffset))
                if len(children) == 3:
                    childOffset = children[2].moonStackOffset
                    if type(childOffset) is int:
                        self.moonLine(None, "addi "+tmpReg+", "+tmpReg+", "+childOffset)
                    else:
                        self.moonLine(None, "add " + tmpReg + ", " + tmpReg + ", " + childOffset)
                        self.registerPool.append(childOffset)
                node.setMoonStackOffset(tmpReg)
            else:
                node.setMoonStackOffset(children[1].moonStackOffset)
        else:
            attName = children[0].value.value
            varNode = node.parent
            while not type(varNode) is VariableNode:
                varNode = varNode.parent
            varEntry = node.findScope(varNode.leftMostChild.value.value)
            classTable = node.findScope(varEntry.entryType).link
            totalOffset = classTable.getTotalEntryOffset(attName, varEntry.offset+self.globalOffset)
            print(totalOffset)
            node.setMoonStackOffset(totalOffset)


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

        # load rhs
        rhsRegister = self.registerPool.pop()
        if not type(children[1]) is IntegerNode:
            rhsRegister = self.loadValFromNodeOffset(children[1].moonStackOffset, rhsRegister)
        else:
            self.moonLine(None, "addi " + rhsRegister + ", R0, " + str(children[1].moonStackOffset))
        # load lhs
        lhsRegister = self.registerPool.pop()
        if not type(children[0]) is IntegerNode:
            lhsRegister = self.loadValFromNodeOffset(children[0].moonStackOffset, lhsRegister)
        else:
            self.moonLine(None, "addi " + lhsRegister + ", R0, " + str(children[0].moonStackOffset))
        self.moonLine(None,op + node.moonRegister + ", " + lhsRegister + ", " + rhsRegister)
        node.setMoonStackOffset(node.symbolTableEntry.offset+self.globalOffset)
        self.moonLine(None, "sw "+ str(node.moonStackOffset)+"("+self.stackRegister+"), "+node.moonRegister)
        self.registerPool.append(rhsRegister)
        self.registerPool.append(lhsRegister)
        self.registerPool.append(node.moonRegister)
        node.setMoonRegister(None)

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
            op = 'div '
        elif node.value.value == 'and':
            op = 'and '
        # load rhs
        rhsRegister = self.registerPool.pop()
        if not type(children[1]) is IntegerNode:
            rhsRegister = self.loadValFromNodeOffset(children[1].moonStackOffset, rhsRegister)
        else:
            self.moonLine(None, "addi " + rhsRegister + ", R0, " + str(children[1].moonStackOffset))
        # load lhs
        lhsRegister = self.registerPool.pop()
        if not type(children[0]) is IntegerNode:
            lhsRegister = self.loadValFromNodeOffset(children[0].moonStackOffset, lhsRegister)
        else:
            self.moonLine(None, "addi " + lhsRegister + ", R0, " + str(children[0].moonStackOffset))
        self.moonLine(None, op + node.moonRegister + ", " + lhsRegister + ", " + rhsRegister)
        node.setMoonStackOffset(node.symbolTableEntry.offset + self.globalOffset)
        self.moonLine(None, "sw " + str(node.moonStackOffset) + "(" + self.stackRegister + "), " + node.moonRegister)
        self.registerPool.append(rhsRegister)
        self.registerPool.append(lhsRegister)
        self.registerPool.append(node.moonRegister)
        node.setMoonRegister(None)

    @visit.register(IntegerNode)
    def _(self, node):
        num = int(node.value.value)
        node.setMoonStackOffset(num)

    @visit.register(VariableNode)
    def _(self, node):
        children = node.getChildrenList()
        var = node.findScope(children[0].value.value)
        if len(children) > 1:
            if type(children[1]) is IndicesNode:
                tmpReg = self.registerPool.pop()
                self.acceptChildren(children[1])
                indicesChildren = children[1].getChildrenList()
                indices = list(map(lambda x: re.sub('\]', '', x), var.entryType.split('[')))
                self.moonLine(None, "addi " + tmpReg + ", R0, 0")
                for i in range(len(indicesChildren)):
                    counter = 1
                    for index in indices[2 + i:]:
                        counter *= int(index)
                    # Load index
                    indexReg = self.registerPool.pop()
                    if type(indicesChildren[i]) is IntegerNode:
                        self.moonLine(None, "addi "+indexReg+", R0, "+str(indicesChildren[i].moonStackOffset))
                    else:
                        self.moonLine(None, "lw "+indexReg+", "+str(indicesChildren[i].moonStackOffset)+"("+self.stackRegister+")")
                    self.moonLine(None, "muli " + indexReg + ", " + indexReg + ", " + str(counter))
                    self.moonLine(None, "add " + tmpReg + ", " + tmpReg + ", " + indexReg)
                    # return index register
                    self.registerPool.append(indexReg)
                self.moonLine(None, "addi " + tmpReg + ", " + tmpReg + ", 1")
                self.moonLine(None,"muli " + tmpReg + ", " + tmpReg + ", " + str(self.typeSizeOf(node, indices[0])))
                self.moonLine(None, "addi " + tmpReg + ", " + tmpReg + ", " + str(var.offset+self.globalOffset))
                node.setMoonStackOffset(tmpReg)
                #self.registerPool.append(tmpReg)
                # self.moonLine(None, "add " + tmpReg + ", " + self.stackRegister + ", " + tmpReg)
                # self.moonLine(None, "lw " + node.moonRegister + ", 0(" + node.moonRegister + ")")
            else:
                children[1].accept(self, True)
                node.setMoonStackOffset(children[1].moonStackOffset)
                children[1].setMoonRegister(None)
        else:
            #varOffset = var.offset+self.globalOffset
            node.setMoonStackOffset(var.offset+self.globalOffset)
            # node.setMoonRegister(self.registerPool.pop())
            # self.moonLine(None, "lw " + node.moonRegister + ", " + str(varOffset) + "(" + self.stackRegister + ")")

    @visit.register(ScopeBlockNode)
    def _(self, node):
        self.moonLine(node.symTable.tag, "nop")
        # adjust for inner scopes
        for entry in node.symTable.entries:
            entry.setOffset(entry.offset - self.globalOffset)
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
        children = node.getChildrenList()
        children[0].accept(self, True)
        ifTag = self.moonTagGenerator()
        elseTag = self.moonTagGenerator()
        endIfTag = self.moonTagGenerator()
        tmpReg = self.registerPool.pop()
        tmpReg = self.loadValFromNodeOffset(children[0].moonStackOffset, tmpReg)
        self.moonLine(None, "bz "+tmpReg+", "+elseTag,  "If Statement")
        children[1].symTable.setTag(ifTag)
        children[1].accept(self, True)
        self.moonLine(None, "j "+ endIfTag)
        children[2].symTable.setTag(elseTag)
        children[2].accept(self, True)
        self.moonLine(endIfTag, "nop", "If statement end")
        self.registerPool.append(tmpReg)

    @visit.register(ForLoopNode)
    def _(self, node):
        children = node.getChildrenList()
        startForTag = self.moonTagGenerator()
        endForTag = self.moonTagGenerator()
        varDeclaredEntry = node.leftMostChild.leftMostChild.symbolTableEntry
        varDeclaredEntry.setOffset(varDeclaredEntry.offset-self.globalOffset)
        # move stack down for declaration
        self.moonLine(None, "subi " + self.stackRegister + ", " + self.stackRegister + ", " + str(node.symTable.entries[0].size),"Alloc stack for for loop declaration scope")
        self.globalOffset += node.symTable.entries[0].size
        #perform decl with assign as it is kind of an exception to the language
        assignNodeRHS = children[0].getChildrenList()[1]
        assignNodeRHS.accept(self, True)
        tmpReg = self.registerPool.pop()
        if not type(assignNodeRHS.moonStackOffset) is int:
            tmpReg = self.loadValFromNodeOffset(assignNodeRHS.moonStackOffset, tmpReg)
        else:
            self.moonLine(None, "addi " + tmpReg + ", R0, " + str(assignNodeRHS.moonStackOffset))
        self.moonLine(None, "sw "+str(varDeclaredEntry.offset+self.globalOffset)+"("+self.stackRegister+"), " + tmpReg)
        node.getChildrenList()[1].accept(self, True)
        tmpReg2 = self.registerPool.pop()
        tmpReg2 = self.loadValFromNodeOffset(children[1].moonStackOffset, tmpReg2)
        self.moonLine(startForTag, "bz " + tmpReg2 + ", " + endForTag)
        children[3].accept(self, True)
        # increment
        children[2].accept(self, True)
        node.getChildrenList()[1].accept(self, True)
        # reload bool expr register
        tmpReg2 = self.loadValFromNodeOffset(children[1].moonStackOffset, tmpReg2)
        self.moonLine(None, 'j '+startForTag)
        self.moonLine(endForTag, "nop", "End of loop")
        #put stack back
        self.globalOffset -= node.symTable.entries[0].size
        self.moonLine(None, "addi " + self.stackRegister + ", " + self.stackRegister + ", " + str(node.symTable.entries[0].size), "Dealloc stack for temp scope")

        self.registerPool.append(tmpReg)
        self.registerPool.append(tmpReg2)

    @visit.register(NotNode)
    def _(self, node):
        self.acceptChildren(node)
        child = node.leftMostChild
        entry = node.symbolTableEntry
        tmpReg = self.registerPool.pop()
        if not type(child) is IntegerNode:
            tmpReg = self.loadValFromNodeOffset(child.moonStackOffset, tmpReg)
        else:
            self.moonLine(None, "addi "+tmpReg+", R0, "+str(child.moonStackOffset))
        self.moonLine(None, "not "+tmpReg+", "+tmpReg)
        node.setMoonStackOffset(entry.offset+self.globalOffset)
        self.moonLine(None, "sw "+str(node.moonStackOffset)+"("+self.stackRegister+"), "+tmpReg)

        self.registerPool.append(tmpReg)

    @visit.register(RelOpNode)
    def _(self, node):
        self.acceptChildren(node)
        tmpReg = ''
        if not node.moonRegister:
            tmpReg = self.registerPool.pop()
        else:
            tmpReg = node.moonRegister
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
        # load rhs
        rhsRegister = self.registerPool.pop()
        if not type(children[1]) is IntegerNode:
            rhsRegister = self.loadValFromNodeOffset(children[1].moonStackOffset, rhsRegister)
        else:
            self.moonLine(None, "addi " + rhsRegister + ", R0, " + str(children[1].moonStackOffset))
        # load lhs
        lhsRegister = self.registerPool.pop()
        if not type(children[0]) is IntegerNode:
            lhsRegister = self.loadValFromNodeOffset(children[0].moonStackOffset, lhsRegister)
        else:
            self.moonLine(None, "addi " + lhsRegister + ", R0, " + str(children[0].moonStackOffset))
        node.setMoonStackOffset(node.symbolTableEntry.offset + self.globalOffset)
        self.moonLine(None, op+" "+tmpReg+", "+lhsRegister+", "+ rhsRegister)
        self.moonLine(None, "sw " + str(node.moonStackOffset) + "(" + self.stackRegister + "), " + tmpReg)
        self.registerPool.append(lhsRegister)
        self.registerPool.append(rhsRegister)
        self.registerPool.append(tmpReg)
        children[0].setMoonRegister(None)
        children[1].setMoonRegister(None)

    @visit.register(PutNode)
    def _(self, node):
        self.acceptChildren(node)
        child = node.leftMostChild
        #load R1
        tmpReg = self.registerPool.pop(0)
        if not type(child) is IntegerNode:
            tmpReg = self.loadValFromNodeOffset(child.moonStackOffset, tmpReg)
        else:
            self.moonLine(None, "addi " + tmpReg + ", R0, " + str(child.moonStackOffset))
        self.moonLine(None, "jl "+self.frameRegister+", putint")
        self.moonLine(None, "addi "+tmpReg+", R0, 10")
        self.moonLine(None, "putc "+tmpReg, "Jump Line")
        child.setMoonRegister(None)
        self.registerPool.insert(0, tmpReg)

    @visit.register(GetNode)
    def _(self, node):
        self.acceptChildren(node)
        child = node.leftMostChild
        # load R1
        tmpReg = self.registerPool.pop(0)
        self.moonLine(None, "jl "+self.frameRegister+", getint")
        #save value
        if type(child.moonStackOffset) is int:
            self.moonLine(None, "sw "+str(child.moonStackOffset)+"("+self.stackRegister+"), "+tmpReg)
        else:
            self.moonLine(None, "add " + child.moonStackOffset + ", " + self.stackRegister + ", " + child.moonStackOffset)
            self.moonLine(None, "sw 0("+child.moonStackOffset+"), "+tmpReg)
            self.registerPool.append(child.moonStackOffset)
        # flush enter key
        self.moonLine(None, "getc " + tmpReg)
        child.setMoonRegister(None)
        self.registerPool.insert(0, tmpReg)

