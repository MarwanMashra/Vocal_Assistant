import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from server import run_server
import multiprocessing

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

path_volume= abspath(__file__)+"_data/"
if __name__ == '__main__':
    face_recognizer("biden.jpg")
    # path_img= path_volume+"faces/obama1.jpg"
    # path_faces= path_volume+"faces.json"
    # path_res= path_volume+"test.txt"
    # os.system("python face_recognizer/__init__.py "+path_img+" "+path_faces+" "+path_res+" "+path_volume)
    
    # p.start()  

    # reponse= "Ok, je lance la musique"
    # text_to_speech(reponse) # synthèse vocale
    # text_to_speech(reponse) # synthèse vocale
    # text_to_speech(reponse) # synthèse vocale
    # text_to_speech(reponse) # synthèse vocale

    # p.terminate()

