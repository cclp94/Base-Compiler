import re
import os
import datetime
from Token import Token 
from LexicalTable import LexicalTable

class LexicalAnalyser:
    LOGS_DIR= './logs/'
    ERROR_FILE = 'error.log'

    def __init__(self, srcCode, filepath):
        self.filepath = filepath 
        self.__src = srcCode
        self.__pointer = 0
        # init table
        self.__table = LexicalTable()

    def __iter__(self):
        return self

    # defines what happens in for loop iterations
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
                # get current index char
                lookup = self.__src[self.__pointer]
                # lookup state
                state = self.__lookupTable(state, lookup)
                if self.__isFinalState(state):
                    if self.__requiresBacktrack(state):
                        self.__pointer -= 1
                    # create token
                    token = self.__createToken(state, initialIndex)
                if self.__checkErrorState(state):
                    # log to error log
                    raise Exception('Invalid Token: '+token.tokenType+ ', '+ token.value+ ' at position '+ str(token.index))
            except TypeError:
                 # log to error log
                err = repr("Type Error: Invalid character: "+self.__src[self.__pointer] + " at position "+ str(self.__pointer))
                self.__fileError(err)
                print(err)
                state = 1
            except Exception as error:
                self.__fileError(repr(error))
                print(repr(error))
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
    def __checkErrorState(self, state):
        return self.__table.isErrorState(state)

    def __fileError(self, errorMsg):
        if not os.path.exists(self.LOGS_DIR):
            os.makedirs(self.LOGS_DIR)
        f = open(self.LOGS_DIR+self.ERROR_FILE, 'a')
        f.write(str(datetime.datetime.utcnow())+": "+ errorMsg+" in "+ self.filepath +"\n")
        f.close()
