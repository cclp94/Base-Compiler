class SymTableLogger:
    out = ''
    inst = None

    def __init__(self, table):
        if not self.inst:
            self.inst = self
        self.inst.log(table)

    @classmethod
    def log(cls, table):
        cls.out += table + '\n'

    @classmethod
    def dump(cls, loc, console):
        f = open(loc, 'w')
        f.write(cls.out)
        f.close()
        if console:
            print(cls.out)