import re

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