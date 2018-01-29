import sys
from LexicalAnalyser import *

src = sys.argv[1]
f_src = open(src)
l = LexicalAnalyser(f_src.read())
for token in l:
    print(token)