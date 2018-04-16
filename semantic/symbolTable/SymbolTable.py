from lexical.Token import Token
from utils.SymTableLogger import SymTableLogger
class SymbolTable:
    def __init__(self, name):
        self.name = name
        self.tag = None
        self.entries = []
        self.offset = 0

    def outputTable(self):
        SymTableLogger(str(self))
        for entry in self.entries:
            if entry.link:
                entry.link.outputTable()

    def setTag(self, tag):
        self.tag = tag

    def addEntry(self, entry):
        self.entries.append(entry)

    def setOffset(self, offset):
        self.offset = offset

    def search(self, identifier):
        # search local table
        for entry in self.entries:
            if type(entry.name) is Token:
                if entry.name.value == identifier:
                    return entry
            elif entry.name == identifier:
                return entry
        # if not found search inner objects
        for entry in self.entries:
            if entry.link:
                result = entry.link.search(identifier)
                if result:
                    return result

    def searchKind(self, entryKind):
        entries = []
        for entry in self.entries:
            if entry.kind == entryKind:
                entries.append(entry)
        return entries

    def getTotalEntryOffset(self, name, offset):
        total = None
        for entry in self.entries:
            if (type(entry.name) is Token and entry.name.value == name) or entry.name == name:
                return offset + entry.offset
            if entry.link:
                total = entry.link.getTotalEntryOffset(name, offset + entry.offset)
                if total:
                    break;
        return total

    def __str__(self):
        string = '-------------------------------------------------------------------------------------\n' + str(self.name) + ' @ ' + hex(id(self)) +'\tScope offset: '+str(self.offset)+'\n'
        for entry in self.entries:
            string += str(entry) + '\n'
        string += '-------------------------------------------------------------------------------------\n'
        return string

class SymbolTableEntry:
    def __init__(self,  name, kind, entryType, link=None):
        self.name = name
        self.kind = kind
        self.entryType = entryType
        self.offset = None
        self.size = None
        self.link = link

    def setLink(self, link):
        self.link = link

    def setOffset(self, offset):
        self.offset = offset

    def setSize(self, size):
        self.size = size

    def __str__(self):
        return '| ' + str(self.name) + ' | ' + str(self.kind) + ' | ' + str(self.entryType) + ' | ' + str(self.size) + ' | ' + str(self.offset) + ' | ' + hex(id(self.link)) + ' |'