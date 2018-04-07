from semantic.visitors.Visitor import *

class CodeGenVisitor(Visitor):

    indent = '          '
    moonCode = ''
    outputLocation = ''
    registerPool = []
    stackRegister = ''
    frameRegister = ''

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

    @methdispatch
    def visit(self, node):
        self.acceptChildren(node)

    @visit.register(ProgramNode)
    def _(self, node):
        self.moonLine(None, "entry", "program entry")
        self.moonLine(None, "align")
        self.moonLine(None, "addi "+self.stackRegister+", R0, topaddr", "init stack pointer register")
        self.moonLine(None, "addi " + self.frameRegister + ", R0, topaddr", "init frame pointer register")
        self.moonLine(None, "addi "+ self.stackRegister+", "+ self.stackRegister+", "+str(node.symTable.offset), "Set stack to top")
        self.acceptChildren(node)
        self.moonLine(None, "hlt", "program exit")
        self.moonLine(None, "END OF PROGRAM")
        #self.moonLine("buf", "res 20", "mem for moon lib subroutines")
        print(self.moonCode)

    @visit.register(AssignNode)
    def _(self, node):
        children = node.getChildrenList()
        lhs = node.findScope(children[0].leftMostChild.value.value)
        lhsOffset = lhs.offset
        lhsRegister = self.registerPool.pop()
        # Right hand side
        rhs = int(children[1].value.value)
        # Assign to register
        self.moonLine(None, "addi "+ lhsRegister+", R0, " + str(rhs))
        self.moonLine(None, "sw "+str(lhsOffset)+"("+self.stackRegister+"), "+lhsRegister)
        self.registerPool.append(lhsRegister)

    @visit.register(PutNode)
    def _(self, node):
        children = node.getChildrenList()
        val = node.findScope(children[0].leftMostChild.value.value)
        valOffset = val.offset
        valRegister = self.registerPool.pop()
        self.moonLine(None, "lw "+valRegister+", "+str(valOffset)+"("+self.stackRegister+")")
        self.moonLine(None, "putc "+valRegister)
        self.registerPool.append(valRegister)

