import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from process import *
from server import run_server
import multiprocessing

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

path_volume= abspath(__file__)+"_data/"
if __name__ == '__main__':
    
    p.start() 
    Tree()
    p.terminate()

