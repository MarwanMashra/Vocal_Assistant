import os,sys
from os.path import dirname
from webcam import Webcam
import docker


if __name__ == '__main__':
    # volumes_path= dirname(__file__)+"/volume"
    volumes={"C:/xampp/htdocs/FDS/S6/HLIN601/TER_S6/_data":{'bind': '/volume', 'mode': 'rw'}}

    # client = docker.from_env()
    # client.containers.run('emo',command='volume/face.jpg volume/emotion.txt',volumes=volumes)
    # Webcam.open()
    # Webcam.take_photo(dirname(__file__)+"/_data")
    # Webcam.close()
    w= Webcam()
    w.open()
    w.take_photo(dirname(__file__)+"/_data")
    w.close()
    # os.system("python ./emotion_recognition/app.py \""+dirname(__file__)+"/.tmp/emotion.txt\"")