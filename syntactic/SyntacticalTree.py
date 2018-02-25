class SyntacticalNode:

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

class SyntacticalTree:
    def __init__(self, value):
        self.root = SyntacticalNode(None, value, False)
