from types import MethodType
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, session, url_for
import pprint,json
from os.path import join,dirname
from sys import platform
import webbrowser

from wsgiref.simple_server import make_server

import sys
from utils import *



TREE_PATH = abspath(__file__)+"/../tree.json"


app= Flask(__name__,
            template_folder=join(abspath(__file__),"template"),
            static_folder=join(abspath(__file__),"static"))

app.config.from_mapping(SECRET_KEY='mysecret')

@app.route('/index.html')
def index():
	return render_template('index.html')


@app.route('/get_tree',methods=['POST'])
def get_tree():
    tree = json.loads(open(TREE_PATH).read())
    return {'tree':tree}

@app.route('/send_tree',methods=['POST'])
def send_tree():
    data = json.loads(request.data.decode('utf-8'))
    tree = data["tree"]
    try:
        with open('tree.json', 'w',encoding='utf8') as outfile:
            json.dump(tree, outfile,indent=4,ensure_ascii=False)
        return "success"
    except:
        return "fail"


def run_server():
    with make_server('',5001,app) as server:
        server.serve_forever()


if __name__ == '__main__' :
    with make_server('',5001,app) as server:
        if(platform.startswith('win')):
            print("Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)")
        else:
            print("Running on http://127.0.0.1:5001/ (Press CTRL+Z to quit)")
        server.serve_forever()


        
        
        

