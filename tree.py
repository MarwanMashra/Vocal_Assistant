import warnings
warnings.filterwarnings("ignore")

import webbrowser
from treetaggerwrapper import TreeTagger, make_tags
from os.path import join
from os import getcwd,popen
import sys
import json
import random
import re

from utils import *

def modif(tree):
    l=[]
    for word in tree['keywords']:
        l.append(word[0]) 
    tree['keywords']=l


def rec(tree):
    if type(tree)==str:
        return
    else:
        modif(tree)
        for t in tree["next"]:
            rec(t)
        return

tree = json.loads(open('tree.json').read())

rec(tree)

print(tree)

with open('tree.json', 'w',encoding='utf8') as outfile:
    json.dump(tree, outfile,indent=4,ensure_ascii=False)


        