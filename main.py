import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from process import *
from server import run_server
import multiprocessing
import json

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

path_volume= abspath(__file__)+"_data/"
keyword= "ok assistant"
list_stop=["fermer","fermeture","annuler","annulation","arrêter","arrêt","terminer","quitter","fin"]

faces = json.loads(open(path_volume+'faces.json').read())

if __name__ == '__main__':

    show= True
    
    p.start() 
    while True:
        if show:
            print("\nJe suis votre assistant, dites: \n[\"ok assistant\"] pour m'appeler \n[\"quitter\"] pour quitter")
            show= False
        speech= speech_to_text()
        if speech:
            if keyword in speech:
                show= True
                Tree()
            else:
                stop= False
                for word in list_stop:
                    if word in speech:
                        stop= True
                if stop:
                    print("Fin de programme...")
                    break   

    p.terminate()
