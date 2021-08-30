import os,time,re,sys
import speech_recognition as sr
from webcam import Webcam
import docker,time,json,bcrypt
from getpass import getpass

EMOTIONS = ['enervé', 'dégoûté', 'apeuré','joyeux', 'triste', 'surpris', 'neutre']

def abspath(file):
    return os.path.abspath(os.path.dirname(file))+"/"

path_volume= abspath(__file__)+"_data/"
volumes={str(path_volume):{'bind': '/volume', 'mode': 'rw'}}

CONFIG_PATH = abspath(__file__)+"config.json"
CREDENTIALS_PATH = abspath(__file__)+"credentials/credentials.json"

config = json.loads(open(CONFIG_PATH).read())

def watch(path_file,t,wait=10):

    # since the time of modification of file is an int, comparasion should be with an int
    t = int(t)
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
        return None

    Webcam.take_photo(path_volume+"face.jpg")
    Webcam.close()

    if not watch(path_volume+"face.jpg",t):
        print("ERROR: cannot take photo")
        return None

    t=time.time()
    client.containers.run('ter_s6_emotion_recognition',command='volume/face.jpg volume/emotion.txt',volumes=volumes,auto_remove=True)

    os.remove(path_volume+"face.jpg")

    if not watch(path_volume+"emotion.txt",t):
        print("ERROR: emotion_recognition cannot detect face or emotion")
        return None

    f= open(path_volume+"emotion.txt","r")
    res= f.readline()
    f.close()
    if not res.isdigit():
        print("ERROR: emotion is not int")
        return None

    os.remove(path_volume+"emotion.txt")

    emotion_index= int(res)

    if emotion_index<0:
        return None
    else:
        return EMOTIONS[emotion_index]

def text_to_speech(text):
    client = docker.from_env()
    text= remove_emojis(text)
    f= open(path_volume+"say.txt","w",encoding='utf-8')
    f.write(text)
    f.close()

    client.containers.run('ter_s6_text_to_speech',command='volume/say.txt volume',volumes=volumes,network_mode="host",auto_remove=True)

    os.remove(path_volume+"say.txt")

def speech_to_text(play_effect="True"):
    client = docker.from_env()
    t=time.time()
    client.containers.run('ter_s6_speech_to_text',command='volume/speech.txt volume '+play_effect,volumes=volumes,network_mode="host",auto_remove=True)

    if not watch(path_volume+"speech.txt",t):
        print("ERROR: speech_to_text")
        return None

    f= open(path_volume+"speech.txt","r")
    speech= f.read()
    f.close()

    os.remove(path_volume+"speech.txt")

    return speech

def face_recognizer(face_path=None,face_bib="faces.json"):

    if not face_path:
        face_path= "face.jpg"
        t=time.time()

        isOpen= Webcam.open()
        if not isOpen:
            print("ERROR: cannot open webcam")
            return None

        Webcam.take_photo(path_volume+face_path)
        Webcam.close()

        if not watch(path_volume+face_path,t):
            print("ERROR: cannot take photo")
            return None

    client = docker.from_env()
    

    t=time.time()
    face_path= "face.jpg"

    client.containers.run('ter_s6_face_recognizer',command='volume/'+face_path+' volume/'+face_bib+' volume/face_reco.txt volume',volumes=volumes,auto_remove=True)
    os.remove(path_volume+face_path)

    if not watch(path_volume+"face_reco.txt",t):
        print("ERROR: face_recognizer cannot detect any face")
        return None

    f= open(path_volume+"face_reco.txt","r")
    name= f.readline()
    f.close()

    os.remove(path_volume+"face_reco.txt")

    return name

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

def str_to_bool(str):
    if str in ["True","true",True,"1",1]:
        return True
    else: 
        return False


def clean_cache():
    for f in os.listdir(path_volume):
        if os.path.isfile(os.path.join(path_volume, f)) and not ".json" in f :
            os.remove(os.path.join(path_volume, f))


def get_os():
    if sys.platform.startswith('win'):
        return "win"
    elif "aarch" in os.popen("uname -m").read():
        return "pi"
    elif sys.platform.startswith('linux'):
        return "linux"
    else:
        return None


def auth():
    if not str_to_bool(config['auth']):
        return True
    else:
        if os.path.exists(CREDENTIALS_PATH):
            logs = json.loads(open(CREDENTIALS_PATH).read())
            hash = logs['password'].encode()
            return check_password(hash,logs['username'])
            
        else:
            password = enter_password()
            hash = bcrypt.hashpw(str(password).encode('utf-8'),bcrypt.gensalt())
            text_to_speech("Veuillez entrer un nom d'utilisateur")
            username = input("Entrez un nom d'utilisateur : ")
            logs={'username':username,'password':str(hash)[2:len(hash)+2]}

            with open(CREDENTIALS_PATH, 'w',encoding='utf8') as outfile:
                json.dump(logs, outfile,indent=4,ensure_ascii=False)

            return True


def enter_password():
    while True:
        text_to_speech("Veuillez entrer un mot de passe d'au moins 6 caractères")
        password = getpass("Entrez le mot de passe (au moins 6 caractères): ")
        if len(password)<6:
            text_to_speech("Le mot de passe est trop court")
            print("mot de passe trop court")
        else:
            text_to_speech("Veuillez confirmer votre mot de passe")
            confirm_password = getpass("Corfirmation du mot de passe : ")
            if password == confirm_password:
                return password
            else:
                text_to_speech("La confirmation ne correspond pas au mot de passe")
                print("Le mot de passe est différent")


def check_password(hash,username,nb_try=3):
    while nb_try:
        nb_try -= 1
        text_to_speech("Veuillez entrer le mot de passe")
        password = getpass("Entrez votre mot de passe : ")
        if bcrypt.hashpw(password.encode('utf-8'),hash)== hash:
            text_to_speech(f"Bonjour {username}")
            return True
        elif nb_try:
            text_to_speech("mot de passe incorrect")
            print(f"Mot de passe incorrect, il vous reste {nb_try} essais")
    return False






