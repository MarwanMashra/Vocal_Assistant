import os,time,sys,re
import speech_recognition as sr
from os.path import dirname
from webcam import Webcam
import docker,time
def abspath(file):
    return os.path.abspath(os.path.dirname(file))+"/"

path_volume= abspath(__file__)+"_data/"
volumes={str(path_volume):{'bind': '/volume', 'mode': 'rw'}}

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
    client = docker.from_env()
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
    client = docker.from_env()
    text= remove_emojis(text)
    f= open(path_volume+"say.txt","w",encoding='utf-8')
    f.write(text)
    f.close()

    client.containers.run('ter_s6_text_to_speech',command='volume/say.txt volume',volumes=volumes,auto_remove=True)

    os.remove(path_volume+"say.txt")

def speech_to_text():
    client = docker.from_env()
    t=time.time()
    client.containers.run('ter_s6_speech_to_text',command='volume/speech.txt volume',volumes=volumes,auto_remove=True)

    if not watch(path_volume+"speech.txt",t):
        print("ERROR: speech_to_text")
        return False,None

    f= open(path_volume+"speech.txt","r")
    speech= f.read()
    f.close()

    os.remove(path_volume+"speech.txt")

    return True,speech

def face_recognizer(face_path="face.jpg"):
    client = docker.from_env()
    client.containers.run('ter_s6_face_recognizer',command='volume/'+face_path+' volume/faces.json volume/test.txt volume',volumes=volumes,auto_remove=False)

def record(file_name):
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        # start recording voice
        print("##### start #####")
        audio = r.listen(source)
        print("###### end ######")
    # save audio file in format wav
    with open(path_volume+file_name, "wb") as f:
        f.write(audio.get_wav_data(convert_rate=16000)) 

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return emoji_pattern.sub(r'', text) # no emoji

