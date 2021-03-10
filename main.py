import os
from os.path import dirname
from webcam import Webcam
import docker
from utils import *
from server import run_server
import multiprocessing

path_volume= abspath(__file__)+"_data/"

if __name__ == '__main__':
    p = multiprocessing.Process(target=run_server, args=())
    p.daemon = True
    p.start() 
    volumes={str(path_volume):{'bind': '/volume', 'mode': 'rw'}}
    client = docker.from_env()
    client.containers.run('ter_s6_text_to_speech',command='volume/myfile.txt volume',volumes=volumes)
    p.terminate()
    
    # if watch(path_volume+"res.txt"):
    #     print("file modified")
    # else:
    #     print("ne changes detected")
    # print(path_abs("_data"))
    # data_path= os.getcwd()+"/_data"
    
    # Webcam.open()
    # Webcam.take_photo(data_path)
    # Webcam.close()

    # t=time.time()
    # wait=10
    # volumes={str(path_volume):{'bind': '/volume', 'mode': 'rw'}}

    
    # client = docker.from_env()
    # client.containers.run('ter_s6_emotion_recognition',command='volume/face.jpg volume/emotion.txt',volumes=volumes)
    # client.containers.run('ter_s6_text_to_speech',command='volume/myfile.txt volume',volumes=volumes)

    # while True:   # wait for the result of emotion_recognition

    #     # result came out 
    #     if (os.stat(data_path+"/emotion.txt")[8] >= t ):   
    #         f= open(data_path+"/emotion.txt","r")
    #         print("Emotion: "+f.readline())
    #         f.close()
    #         break

    #     # time out and no result yet
    #     if (time.time() > t+wait):
    #         print("Timeout, no emotion has been detected")
    #         break

