class Token:
    def __init__(self, tokenType, value, index):
        self.tokenType = tokenType
        self.value = value
        self.index = index

    def __str__(self):
        return repr("["+self.tokenType + ":" + self.value+"]")

    def serialize(self):
        #return "["+self.tokenType + ":" + repr(self.value)+":"+str(self.index)+"]\n"
        return self.tokenType