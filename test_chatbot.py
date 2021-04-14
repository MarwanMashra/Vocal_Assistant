
import warnings
warnings.filterwarnings("ignore")

import os,sys
from os.path import dirname
from webcam import Webcam
import docker,time
from utils import *
from server import run_server
import multiprocessing
from chatbot import chatbot

from process import process

p = multiprocessing.Process(target=run_server, args=())
p.daemon = True

EMOTIONS = ['enervé', 'dégoûté', 'apeuré','joyeux', 'triste', 'surpris', 'neutre']
if __name__ == '__main__':    

    p.start()  

    # while True:
    speech= speech_to_text()
    if speech:
        response= chatbot(speech)
        if response:
            text_to_speech(response)
        else:
            text_to_speech("ça ne marche pas encore")

    p.terminate()

