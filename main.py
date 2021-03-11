import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from server import run_server
import multiprocessing

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

EMOTIONS = ['enervé', 'dégoûté', 'apeuré','joyeux', 'triste', 'surpris', 'neutre']

if __name__ == '__main__':    
    p.start()  

    val,index= emotion_recognition()   # reconnaissance des émotions
    if val:

        phrase = "Vous avez l'aire "+EMOTIONS[index]+". Vous voulez écouter de la musique ?"
        text_to_speech(phrase)    # synthèse vocale

        val,speech= speech_to_text() # reconnaissace de la parole

        if val:
        
            if speech=="oui":
                reponse= "Ok, je lance la musique"
            elif speech=="non":
                reponse= "tant pis"
            else:
                reponse= "je n'ai pas compris"

            text_to_speech(reponse) # synthèse vocale

    p.terminate()
