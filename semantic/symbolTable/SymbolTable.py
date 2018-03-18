from lexical.Token import Token

class SymbolTable:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def addEntry(self, entry):
        self.entries.append(entry)

    def search(self, identifier):
        for entry in self.entries:
            if type(entry.name) is Token:
                if entry.name.value == identifier:
                    return entry
            elif entry.name == identifier:
                return entry

    def __str__(self):
        string = '-------------------------------------------------------------------------------------\n' + str(self.name) + ' @ ' + hex(id(self)) +'\n'
        for entry in self.entries:
            string += str(entry) + '\n'
        string += '-------------------------------------------------------------------------------------\n'
        return string

class SymbolTableEntry:
    def __init__(self,  name, kind, entryType, link=None):
        self.name = name
        self.kind = kind
        self.entryType = entryType
        self.link = link

    def setLink(self, link):
        self.link = link


    def __str__(self):
        return '| ' + str(self.name) + ' | ' + str(self.kind) + ' | ' + str(self.entryType) + ' | ' + hex(id(self.link)) + ' |'