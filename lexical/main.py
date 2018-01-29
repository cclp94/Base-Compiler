import sys
from LexicalAnalyser import *

OUTPUT_FILE = "./logs/output.txt"

def showUsage(msg):
    print("ERROR: "+msg+":\n\
    Usage: py Main.py -f <file path>\
     -o\n-f <file path>: source code to analyse\n\
     -o: generate output on log [optional]")

try:
    arg_count = len(sys.argv)
    if(arg_count > 1):
        flag = sys.argv[1]
        if flag == '-f':
            print(sys.argv[2])
            out = None
            src = open(sys.argv[2]).read()
            if arg_count == 4:
                out = open(OUTPUT_FILE, 'w')
            l = LexicalAnalyser(src)
            for token in l:
                print(token)
                if out:
                    out.write(token.serialize())
            if out:
                out.close()
        else:
            raise Exception('Wrong argumets')
    else:
        raise Exception('Wrong argumets')
except IOError:
    showUsage("File not found")
except Exception as error:
    showUsage(repr(error))