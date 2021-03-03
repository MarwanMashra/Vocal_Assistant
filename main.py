import os,sys
from os.path import dirname
from webcam import Webcam
import docker


if __name__ == '__main__':
    
    Webcam.open()
    Webcam.take_photo(os.getcwd()+"/_data")
    Webcam.close()

    volumes={os.getcwd()+"/_data":{'bind': '/volume', 'mode': 'rw'}}
    
    client = docker.from_env()
    client.containers.run('ter_s6_emotion_recognition',command='volume/face.jpg volume/emotion.txt',volumes=volumes)
