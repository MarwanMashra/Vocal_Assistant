import webbrowser
from treetaggerwrapper import TreeTagger, make_tags
from os.path import join
from os import getcwd
import sys
import json

intents = json.loads(open('intents.json').read())

if sys.platform.startswith('linux'):
    tagger = TreeTagger(TAGLANG='fr',TAGDIR=join(getcwd(),'Treetagger','TreeTagger_unix'))
elif sys.platform.startswith('win'):
    tagger = TreeTagger(TAGLANG='fr',TAGDIR=join(getcwd(),'Treetagger','TreeTagger_windows'))
else:
    sys.exit('Système d\'exploitation non compatible.')

def process(text):

    return take_action(text)

def take_action(text):
    tag,start,end= get_tag(text)

    if tag=="google":
        res= "Je cherche sur google"
        url = 'https://www.google.com/search?q='+text[end:].strip().replace(' ','+')
        webbrowser.open_new_tab(url)
    elif tag=="wiki":
        res= "je cherche sur wikipédia"
    elif tag=="youtube":
        res= "Je cherche sur Youtube"
        url= "https://www.youtube.com/results?search_query="+text[end:].strip().replace(' ','+')
        webbrowser.open_new_tab(url)
    elif tag=="image":
        res= "j'ouvre une image"
    elif tag=="music":
        res= "je lance un music"
    else:
        res= "je ne suis pas encore programmé pour ça"

    return res

def get_tag(text):
    tags = make_tags(tagger.tag_text(text),exclude_nottags=True)
    print(tags)
    proper_name=[]
    noun=[]
    verb=[]
    for index,(word,pos,lemma) in enumerate(tags):
        lemma=lemma.lower()
        if ( pos=="NAM" or pos=="ADJ") and (lemma,word) not in proper_name:
            proper_name.append((lemma,word))
        elif pos=="NOM" and (lemma,word) not in noun:
            noun.append((lemma,word))
        elif pos.startswith("VER") and (lemma,word) not in verb:
            verb.append((lemma,word))
    
    list_tags= proper_name+noun+verb
    print(list_tags)
    for word in list_tags:
        for category in intents['intents']:
            if word[0] in category['keywords']:
                return category['tag'],text.find(word[1]),text.find(word[1])+len(word[1])
    for word in list_tags:
        for category in intents['intents']:
            if word[0] in category['patterns']:
                return category['tag'],text.find(word[1]),text.find(word[1])+len(word[1])

    return None,None,None



# url = 'http://docs.python.org/'
# webbrowser.open_new_tab(url)


# if platform.startswith('linux'):
# 	with context(join('Treetagger','TreeTagger_unix')):
# 		run(['./install-tagger.sh'],check=True)
# 	print('Installation de l\'étiqueteur TreeTagger réussie.')
