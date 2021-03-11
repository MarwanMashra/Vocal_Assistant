import os,time,sys
from os.path import dirname
from webcam import Webcam
import docker,time
def abspath(file):
    return os.path.abspath(os.path.dirname(file))+"/"

path_volume= abspath(__file__)+"_data/"
volumes={str(path_volume):{'bind': '/volume', 'mode': 'rw'}}
client = docker.from_env()

def watch(path_file,t,wait=10):
    if wait>100:
        print("ERROR: wait should be < 100")
        return False

    while True:   # wait for the result of emotion_recognition

        # result came out 
        if (os.path.isfile(path_file) and (os.stat(path_file)[8] >= t)):   
            return True

        # time out and no result yet
        if (time.time() > t+wait):
            print("Timeout")
            return False

def emotion_recognition():

    t=time.time()

    isOpen= Webcam.open()
    if not isOpen:
        print("ERROR: cannot open webcam")
        return False,None

    Webcam.take_photo(path_volume+"face.jpg")
    Webcam.close()

    if not watch(path_volume+"face.jpg",t):
        print("ERROR: cannot take photo")
        return False,None

    t=time.time()
    client.containers.run('ter_s6_emotion_recognition',command='volume/face.jpg volume/emotion.txt',volumes=volumes,auto_remove=True)

    os.remove(path_volume+"face.jpg")

    if not watch(path_volume+"emotion.txt",t):
        print("ERROR: emotion_recognition cannot detect face or emotion")
        return False,None

    f= open(path_volume+"emotion.txt","r")
    res= f.readline()
    f.close()
    if not res.isdigit():
        print("ERROR: emotion is not int")
        return False,None

    os.remove(path_volume+"emotion.txt")

    return True,int(res)

def text_to_speech(text):

    f= open(path_volume+"say.txt","w",encoding='utf-8')
    f.write(text)
    f.close()

    client.containers.run('ter_s6_text_to_speech',command='volume/say.txt volume',volumes=volumes,auto_remove=True)

    os.remove(path_volume+"say.txt")

def speech_to_text():
    t=time.time()
    client.containers.run('ter_s6_speech_to_text',command='volume/speech.txt volume',volumes=volumes,auto_remove=True)

    if not watch(path_volume+"speech.txt",t):
        print("ERROR: speech_to_text")
        return False,None

    f= open(path_volume+"speech.txt","r")
    speech= f.read().replace('\n',' ').strip()
    f.close()

    os.remove(path_volume+"speech.txt")

    return True,speech
