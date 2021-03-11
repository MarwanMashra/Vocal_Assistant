import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from server import run_server
import multiprocessing

EMOTIONS = ['enervé', 'dégoûté', 'apeuré','joyeux', 'triste', 'surpris', 'neutre']


path_volume= abspath(__file__)+"_data/"
volumes={str(path_volume):{'bind': '/volume', 'mode': 'rw'}}

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

client = docker.from_env()

if __name__ == '__main__':
    
    p.start()  

    t=time.time()

    Webcam.open()
    Webcam.take_photo(path_volume+"face.jpg")
    Webcam.close()

    if not watch(path_volume+"face.jpg",t):
        print("ERROR: webcam")
        p.terminate()
        sys.exit()

    t=time.time()
    client.containers.run('ter_s6_emotion_recognition',command='volume/face.jpg volume/emotion.txt',volumes=volumes,auto_remove=True)

    if not watch(path_volume+"emotion.txt",t):
        print("ERROR: emotion_recognition")
        p.terminate()
        sys.exit()

    f= open(path_volume+"emotion.txt","r")
    res= f.readline()
    if not res.isdigit():
        print("ERROR: emotion is not int")
        p.terminate()
        sys.exit()

    emotion = EMOTIONS[int(res)]

    phrase = "Vous avez l'aire "+emotion+". Vous voulez écouter de la musique ?"

    f= open(path_volume+"say.txt","w")
    f.write(phrase)
    f.close()

    client.containers.run('ter_s6_text_to_speech',command='volume/say.txt volume',volumes=volumes,auto_remove=True)

    t=time.time()
    client.containers.run('ter_s6_speech_to_text',command='volume/speech.txt volume',volumes=volumes,auto_remove=True)

    if not watch(path_volume+"speech.txt",t):
        print("ERROR: speech_recognition")
        p.terminate()
        sys.exit()

    f= open(path_volume+"speech.txt","r")
    speech= f.read().replace('\n',' ').strip()
    f.close()

    if speech=="oui":
        reponse= "Ok, je lance la musique"
    elif speech=="non":
        reponse= "tant pis"
    else:
        reponse= "je n'ai pas compris"

    f= open(path_volume+"say.txt","w")
    f.write(reponse)
    f.close()

    client.containers.run('ter_s6_text_to_speech',command='volume/say.txt volume',volumes=volumes,auto_remove=True)

    p.terminate()

