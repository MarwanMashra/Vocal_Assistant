
import speech_recognition as sr
import sys,os,requests


if sys.platform.startswith('win'):
    DEFAULT_HOST= "host.docker.internal"
else:
    DEFAULT_HOST= "127.0.0.1"

DEFAULT_PORT= "5000"

def url(route="",host=DEFAULT_HOST,port=DEFAULT_PORT):
    return 'http://'+host+':'+port+'/'+route

def convert_text(path_text,path_volume,play_effect=True):
    # information about the file audio
    file_name="audio.mp3"
    file_path=path_volume+"/"+file_name

    # send a request to record audio form mic
    response= requests.get(url("microphone"),params={'file':file_name,'play_effect':play_effect}).json() 

    if response['status']=='succes':
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            # read the entire audio file
            audio = r.listen(source)  
            try:
                # try converting the audio into text
                text = r.recognize_google(audio, language="fr-FR")
                # write the text in the text file
                f= open(path_text,"w")
                f.write(text)
                f.close()
            except Exception as e:
                print("Exception: " + str(e))

        # delete audio file
        os.remove(file_path)
    else:
        print("ERROR in convert_text :")
        print(response["error"])


if __name__ == "__main__":
    if len(sys.argv)==3:
        convert_text(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==4:
        convert_text(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print("--------------------\nSpeech Recognition:\n--------------------")
        print("python ./__init__.py [path_text] [path_volume]")
        print("[path_text]: the path of the text file in which result will be stored")
        print("[path_volume]: the path of the shared directory that this container can access\n")
        print("[rec_effect]: (optional) a bool to whether or not play a soound effect when start recoding (DEFAULT: True)\n")
