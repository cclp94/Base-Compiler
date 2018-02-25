import sys
import os
from lexical.LexicalAnalyser import *
from syntactic.SyntacticalAnalyser import parse

OUTPUT_FILE = "lexical/logs/output.txt"

def showUsage(msg):
    print("ERROR: "+msg+":\nUsage: py Main.py -f <file path> -o\n-f <file path>: source code to analyse\n-o: generate output on log [optional]")

#try:
#get argument count
arg_count = len(sys.argv)
# if num of arguments is correct
if(arg_count > 1):
    flag = sys.argv[1]
    # check if -f flag is present
    if flag == '-f':
        # get file path
        filepath =sys.argv[2]
        out = None
        # open file
        f = open(filepath, 'r')
        src = f.read()
        f.close()
        # check if -o flag was present, if so create logs folder and create output file
        if arg_count == 4:
            if not os.path.exists("lexical/logs/"):
                os.makedirs("lexical/logs/")
            out = open(OUTPUT_FILE, 'w')
        #initialize Lexical Analyser
        l = LexicalAnalyser(src, filepath)
        # iterate through Token Stream
        print(parse(l))
        # for token in l:
        #     print(token)
        #     if out:
        #         # generate output file
        #         out.write(token.serialize() + ' ')
        # if out:
        #     out.write('EOU')
        #     out.close()
#     else:
#         raise Exception('Wrong argumets')
# else:
#     raise Exception('Wrong argumets')
# except Exception as error:
#     showUsage(repr(error))