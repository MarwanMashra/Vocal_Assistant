from gtts import gTTS 
import os,requests,sys

DEFAULT_HOST= "host.docker.internal"
DEFAULT_PORT= "5000"

def url(route="",host=DEFAULT_HOST,port=DEFAULT_PORT):
    return 'http://'+host+':'+port+'/'+route

    
def convert_audio(path_text,path_volume):
        
    language = 'fr'
    file_name="audio.mp3"
    # extract text from file
    with open(path_text, 'r') as f:
        text = f.read().replace('\n',' ')

    if text=="":
        return

    # generate audio file from text
    myobj = gTTS(text=text, lang=language, slow=False)
    file_path=path_volume+'/'+file_name
    myobj.save(file_path) 
    
    # ask server to play the audio file
    response= requests.get(url("playsound"),params={'file':file_name}).json()  

    # delete the audio file
    os.remove(file_path)
    
    if(response["status"]=="fail"):
        # show the error message
        print("ERROR in convert_audio :")
        print(response["error"])
                

if __name__ == '__main__':
    if len(sys.argv)==3:
        convert_audio(sys.argv[1],sys.argv[2])
    else:
        print("--------------------\nText to Speech:\n--------------------")
        print("python ./app.py [path_text] [path_volume]")
        print("[path_text]: the path of the text file to convert")
        print("[path_volume]: the path of the shared directory that this container can access\n")
    
