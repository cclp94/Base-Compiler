import sys
import os
from lexical.LexicalAnalyser import *
from syntactic.SyntacticalAnalyser import parse

LEXICAL_OUTPUT_FILE = "./logs/lexical/output.log"
SYNTACTICAL_OUTPUT_FILE = "./logs/syntactical/output.log"
SYNTACTICAL_ERROR_FILE = "./logs/syntactical/error.log"

def showUsage(msg):
    print("ERROR: "+msg+":\nUsage: py Main.py -f <file path> -o\n-f <file path>: source code to analyse\n-o: generate output on log [optional]")

#get argument count
arg_count = len(sys.argv)
# if num of arguments is correct
if(arg_count > 1):
    flag = sys.argv[1]
    # check if -f flag is present
    if flag == '-f':
        # get file path
        filepath =sys.argv[2]
        lexOut = None
        synOut = None
        synErrOut = None
        # open file
        f = open(filepath, 'r')
        src = f.read()
        f.close()
        # check if -o flag was present, if so create logs folder and create output file
        if arg_count == 4:
            if not os.path.exists("./logs/"):
                os.makedirs("./logs/")
            if not os.path.exists("./logs/syntactical/"):
                os.makedirs("./logs/syntactical/")
            if not os.path.exists("./logs/lexical/"):
                os.makedirs("./logs/lexical/")
            lexOut = open(LEXICAL_OUTPUT_FILE, 'w')
            synOut = open(SYNTACTICAL_OUTPUT_FILE, 'w')
            synErrOut = open(SYNTACTICAL_ERROR_FILE, 'w')
        #initialize Lexical Analyser
        l = LexicalAnalyser(src, filepath, lexOut)
        parse(l, synOut, synErrOut)
        if lexOut:
            lexOut.close()
        if synOut:
            synOut.close()