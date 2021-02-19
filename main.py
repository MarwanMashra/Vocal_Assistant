import os,sys
from os.path import dirname

if __name__ == '__main__':
    os.system("python ./emotion_recognition/app.py \""+dirname(__file__)+"/.tmp/emotion.txt\"")