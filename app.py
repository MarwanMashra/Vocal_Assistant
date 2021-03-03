# test comment
#ceci est un changement
from tkinter import *

from gtts import gTTS 

from playsound import playsound

import speech_recognition as sr

import os

from webcam_utils import get_current_emotion

EMOTIONS = ['Angry', 'Disgusted', 'Fearful', 'Happy', 'Sad', 'Surprised', 'Neutral']

def convert_audio():
    
    address_info = address.get()
    
    language = 'fr'
    
    myobj = gTTS(text=address_info, lang=language, slow=False)
    
    myobj.save("_data/audio.mp3") 
    
    playsound("_data/audio.mp3")

    os.remove("_data/audio.mp3")
    
        
    print(address_info)
    
    address_entry.delete(0,END)    
    
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="fr-FR")
            print(said)
            parole_str.set("Vous avez dit : "+said)
        except Exception as e:
            print("Exception: " + str(e))
            parole_str.set("Vous avez dit : "+" ERROR")

    return said

def get_txt():
    txt = get_audio()
    f= open("_data/myfile.txt","w+")
    f.write(txt)
    f.close()

def get_emotion():
    emotion_str.set("Emotion : "+EMOTIONS[get_current_emotion()])


if __name__ == "__main__":
    # run_realtime_emotions()
    # prepare_realtime_emotions()
    # print(EMOTIONS[get_current_emotion()])
    app = Tk()

    app.geometry("500x500")

    app.title("Ter S6")

    heading = Label(text="Application de démo",bg="yellow",fg="black",font="10",width="500",height="3")

    heading.pack()

    address_field = Label(text="Text :")

    address_field.place(x=15,y=70)

    address = StringVar()


    address_entry = Entry(textvariable=address,width="30")

    address_entry.place(x=15,y=100)

    button = Button(app,text="Convertir en audio",command=convert_audio,width="30",height="2",bg="grey")

    button.place(x=15,y=140)

    button = Button(app,text="Appuyer pour parler",command=get_txt,width="30",height="2",bg="red")

    button.place(x=15,y=300)

    parole_str = StringVar()
    parole_str.set("Vous avez dit : ....")

    address_field = Label(textvariable=parole_str)

    address_field.place(x=15,y=250)


    # ############
    button = Button(app,text="Lire emotion",command=get_emotion,width="30",height="2",bg="red")

    button.place(x=15,y=350)

    emotion_str = StringVar()
    emotion_str.set("Emotion : ....")
    address_field = Label(textvariable=emotion_str)
    address_field.place(x=15,y=400)

    app.mainloop()