import re

class Token:
    def __init__(self, tokenType, value, index):
        self.tokenType = tokenType
        self.value = value
        self.index = index

    def __str__(self):
        return repr("["+self.tokenType + ":" + self.value+"]")

class LexicalAnalyser:
    def __init__(self, srcCode):
        self.__src = srcCode
        self.__pointer = 0
        # init table
        self.__table = LexicalTable()

    def __iter__(self):
        return self

    def __next__(self):
        token = self.nextToken()
        if not token or len(self.__src)-1 == self.__pointer:
            raise StopIteration
        return token

    def nextToken(self):
        state = 1
        token = None
        
        while not token and self.__pointer < len(self.__src):
            try:
                if state == 1:
                    initialIndex = self.__pointer
                lookup = self.__src[self.__pointer]
                state = self.__lookupTable(state, lookup)
                if self.__isFinalState(state):
                    if self.__requiresBacktrack(state):
                        self.__pointer -= 1
                    token = self.__createToken(state, initialIndex)
            except TypeError:
                print(repr("Type Error: Invalid character: "+self.__src[self.__pointer] + " at position "+ str(self.__pointer)))
                state = 1
            self.__pointer += 1
        return token

    def __lookupTable(self, state, lookup):
        return self.__table.lookup(state, lookup)
    def __isFinalState(self, state):
        return self.__table.checkFinal(state)
    def __createToken(self, state, index):
        tokenType = self.__table.checkFinal(state)
        value = self.__src[index:self.__pointer+1]
        if self.__table.checkKeyword(value):
            return Token('KEYWORD', value, index)
        return Token(tokenType, value, index)
    def __requiresBacktrack(self, state):
        return self.__table.requiresBacktrack(state)

class LexicalTable:
    TABLE_RESOURCE_LOC = './resources/lexicalTable.csv'
    KEYWORDS_RESOURCE_LOC = './resources/keywords.txt'

    def __init__(self):
        self.__generateTable()
        self.__generateKeywords()

    def __generateTable(self):
        f = open(self.TABLE_RESOURCE_LOC, 'r')
        self.__table = {}
        line = f.readline()
        order = []
        p = re.compile("\\\\(.*)\\\\")
        for cell in line.split('|'):
            c = cell.strip()
            key = p.sub('', c)
            self.__table[key] = [p.search(c).group(1)]
            order.append(key)
        for line in f.readlines():
            cells = line.split('|')
            for i in range(0, len(order)):
                self.__table[order[i]].append(cells[i].strip())
        f.close()
    def __generateKeywords(self):
        f = open(self.KEYWORDS_RESOURCE_LOC, 'r')
        self.__keywords = []
        for line in f.readlines():
            self.__keywords.append(line.strip())
    
    def checkKeyword(self, candidate):
        return candidate in self.__keywords
    
    def lookup(self, state, lookup):
        for key in self.__table.keys():
            p = re.compile(self.__table[key][0])
            if p.search(lookup) and len(p.search(lookup).group()):
                #print(lookup + ", "+ str(state) + "->"+ self.__table[key][state])
                return int(self.__table[key][state])
    
    def checkFinal(self, state):
        token = self.__table['token'][state]
        if token == 'FALSE':
            return False
        else:
            return token

    def requiresBacktrack(self, state):
        back = self.__table['back'][state]
        if back == 'TRUE':
            return True
        else:
            return False
