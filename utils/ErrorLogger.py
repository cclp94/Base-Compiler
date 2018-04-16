import datetime

class ErrorLogger:
    errorLog = ''
    inst = None

    def __init__(self, logLine):
        if not self.inst:
            self.inst = self
        self.inst.log(logLine)

    @classmethod
    def log(cls, line):
        cls.errorLog += str(datetime.datetime.utcnow())+": "+line + '\n'

    @classmethod
    def dump(cls, loc, console):
        f = open(loc, 'w')
        f.write(cls.errorLog)
        f.close()
        if console:
            print(cls.errorLog)