import os,sys,time
from os.path import dirname
from webcam import Webcam
import docker


if __name__ == '__main__':
    
    data_path= os.getcwd()+"/_data"
    
    Webcam.open()
    Webcam.take_photo(data_path)
    Webcam.close()

    t=time.time()
    wait=10
    volumes={str(data_path):{'bind': '/volume', 'mode': 'rw'}}
    
    client = docker.from_env()
    client.containers.run('ter_s6_emotion_recognition',command='volume/face.jpg volume/emotion.txt',volumes=volumes)

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

