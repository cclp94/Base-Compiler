import sys
import subprocess
import os.path

class Moon:
    MOON_PATH = './moon/moon.exe'
    def __init__(self, src):
        if not os.path.isfile(self.MOON_PATH):
            subprocess.call(['gcc', '-o', 'moon', self.MOON_PATH+'.c'])
        self.__exec__(src)

    def  __exec__(self, src):
        subprocess.call([self.MOON_PATH, src, '+t'])

