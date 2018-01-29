class Token:
    def __init__(self, tokenType, value, index):
        self.tokenType = tokenType
        self.value = value
        self.index = index

    def __str__(self):
        return repr("["+self.tokenType + ":" + self.value+"]")