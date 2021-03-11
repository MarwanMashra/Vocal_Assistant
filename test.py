import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from server import run_server
import multiprocessing

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

client = docker.from_env()

if __name__ == '__main__':
    
    p.start()  

    reponse= "Ok, je lance la musique"
    text_to_speech(reponse) # synthèse vocale
    text_to_speech(reponse) # synthèse vocale
    text_to_speech(reponse) # synthèse vocale
    text_to_speech(reponse) # synthèse vocale

    p.terminate()

