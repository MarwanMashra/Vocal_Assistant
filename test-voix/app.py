from gtts import gTTS 
import os
from playsound import playsound

def convert_audio(text):
        
    language = 'fr'
    
    myobj = gTTS(text=text, lang=language, slow=False)
    
    myobj.save("audio.mp3") 
    
    playsound("audio.mp3")

    os.remove("audio.mp3")
    
print("salut")
convert_audio("salut")