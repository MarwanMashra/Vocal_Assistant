import warnings
warnings.filterwarnings("ignore")

import webbrowser
from treetaggerwrapper import TreeTagger, make_tags
from os.path import join
from os import getcwd,popen
import sys
import json
import random
import re

from utils import *

EXIT_TREE= 1
REPETE= 2

CONFIG_PATH = abspath(__file__)+"config.json"

path_volume= abspath(__file__)+"_data/"

tree = json.loads(open('tree.json').read())
faces = json.loads(open(path_volume+'faces.json').read())
config = json.loads(open(CONFIG_PATH).read())


my_os = get_os()
if my_os=='win':
    tagger = TreeTagger(TAGLANG='fr',TAGDIR=join(getcwd(),'Treetagger','TreeTagger_windows'))
elif my_os=='pi':
    tagger = TreeTagger(TAGLANG='fr',TAGDIR=join(getcwd(),'Treetagger','TreeTagger_pi'))
elif my_os=='linux':
    tagger = TreeTagger(TAGLANG='fr',TAGDIR=join(getcwd(),'Treetagger','TreeTagger_unix'))
else:
    sys.exit('Système d\'exploitation non compatible.')


def Tree(tree=tree):


    clean_cache()

    # if tree is a tag, search it
    if type(tree)==str:
        tree= get_tree_by_tag(tree)
        if not tree:
            return
    

    if not str_to_bool(config['screen_mode']) and "screen" in tree['config']:
        text_to_speech("Cette action n'est pas possible car le mode écran est désactivé")
        return "start"

    text= tree['text']
    say=""

    # Do a random choices of sentences to say
    for choices in text:  
        choice= random.choice(choices)
        say+= analyse_var(choice,tree)

        # add an end of sentence point where needed
        if say.strip()[-1]!="?" and say.strip()[-1]!="!":
            say+=","

    text_to_speech(say)

    # Chose the next step based on the request of the user 
    step= next_step(tree)

    # stop the fonction if the user asked for
    if step==EXIT_TREE:
        return
    else:
        Tree(step)


def analyse_var(text,tree):
    variables = re.findall(r"(\{(.+?)\})", text)
    for string,var in variables:
        var = var.strip().lower()
        if var=="context":
            value=tree['context']
        else:
            value=string
        text= text.replace(string,value,1)

    return text

def next_step(tree):
    action= tree['action']
    step=None

    if action=="listen":
        response= listen()
        if response:
            step= choose_next_step(response,tree)
            if step==REPETE:
                Tree(tree)
                step= EXIT_TREE

    elif action=="face_recognizer":
        res= face_recognizer()
        if res=="0":
            step= choose_next_step("unknown",tree)
        else:
            step= choose_next_step("known",tree,context=res)
    
    elif action=="emotion_recognition":
        emotion = emotion_recognition()
        if emotion:
            step= choose_next_step("known",tree,context=emotion)
        else:
            step= choose_next_step("unknown",tree)

    elif action=="face_register":
        isOpen= Webcam.open()
        if isOpen:
            Webcam.take_photo(path_volume+"user.jpg")
            Webcam.take_photo(path_volume+"face.jpg")
            Webcam.close()

            succes= bool(int(face_recognizer("face.jpg","user.jpg")))
            if succes:
                text_to_speech("Quel est votre nom ?")
                name= listen()
                if name:
                    if name not in [f['name'] for f in faces['faces']]: 
                        path_img= "faces/"+name.strip().replace(' ','_')+".jpg"
                        os.rename(path_volume+"user.jpg",path_volume+path_img)

                        faces['faces'].append({'name': name, 'path_img': path_img})
                        jsonFile = open(path_volume+"faces.json", "w+")
                        jsonFile.write(json.dumps(faces,indent=4))
                        jsonFile.close()

                        step= choose_next_step("succes",tree) 
                    else:            
                        text_to_speech("Désolé, ce nom existe déjà, j'annule cette opération")
                else:
                    text_to_speech("Désolé, je n'ai pas compris, j'annule cette opération")

                if not step:
                    os.remove(path_volume+"user.jpg")
                    step= "start"

            else:
                step= choose_next_step("fail",tree)

        else:
            text_to_speech("Désolé, je n'ai pas pu ouvrir le webcam")
            step= "start"

    elif action=="google":
        attempt=3
        request = speech_to_text()
        while not request or request=="":
            if attempt:
                attempt-= 1
                text_to_speech("Je n'ai pas compris, pouvez-vous répéter ?")
                request = speech_to_text()
            else:
                break

        if request and request!="":
            text_to_speech(random.choice(["Voici les résultats","Voici ce que j'ai trouvé"])) 
            url = 'https://www.google.com/search?q='+request.strip().replace(' ','+')
            webbrowser.open_new_tab(url)

        else: 
            text_to_speech("Désolé, je n'ai pas compris")

        step= "start"  

    elif action=="youtube":
        attempt=3
        request = speech_to_text()
        while not request or request=="":
            if attempt:
                attempt-= 1
                text_to_speech("Je n'ai pas compris, pouvez-vous répéter ?")
                request = speech_to_text()
            else:
                break

        if request and request!="":
            text_to_speech(random.choice(["Voici les résultats","Voici ce que j'ai trouvé"])) 
            url = 'https://www.youtube.com/search?q='+request.strip().replace(' ','+')
            webbrowser.open_new_tab(url)
        else: 
            text_to_speech("Désolé, je n'ai pas compris")

        step= "start" 
            
    elif action=="stop":
        step= EXIT_TREE

    else:
        step= random.choice(tree['next'])

    return step


def choose_next_step(text,tree,context=None):
    responses= tree['next']
    responses.append("start>stop")
    
    tags = make_tags(tagger.tag_text(text),exclude_nottags=True)
    proper_name=[]
    noun=[]
    verb=[]
    other=[]
    for index,(word,pos,lemma) in enumerate(tags):
        lemma=lemma.lower()
        if ( pos=="NAM" or pos=="ADJ") and lemma not in proper_name:
            proper_name.append(lemma)
        elif pos=="NOM" and lemma not in noun:
            noun.append(lemma)
        elif pos.startswith("VER") and lemma not in verb:
            verb.append(lemma)
        else:
            other.append(lemma)


    list_tags= proper_name+noun+verb+other

    # check for other keywords
    for tag in list_tags:
        for response in responses:
            if type(response)==str:
                response= get_tree_by_tag(response)
            if tag in response['keywords']:
                if context:
                    response['context']=context
                return response

    # cannot find an anwser in the middle of an action => REPETE
    text_to_speech("Désolé, je n'ai pas compris")
    return REPETE

def get_tree_by_tag(tag):
    list_tree= extract_tree(tree)
    for t in list_tree:
        if tag==t['tag']:
            return t
    return None

def extract_tree(tree):
    if type(tree)==str:
        return []
    else:
        l=[]
        l.append(tree)
        for t in tree["next"]:
            l+= extract_tree(t)
        return l
        

def listen():
    attempt=3
    response = speech_to_text()
    while not response:
        if attempt:
            attempt-= 1
            text_to_speech("Je n'ai pas compris, pouvez-vous répéter ?")
            response = speech_to_text()
        else:
            break

    return response
