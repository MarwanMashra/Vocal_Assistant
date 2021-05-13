import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import cv2
import random
import pickle
import progressbar

training_data = []
EMOTIONS = ['Angry', 'Disgusted', 'Fearful','Happy', 'Sad', 'Surprised', 'Neutral']
DATADIR="data/training"
IMG_SIZE= 48

total_img = 0
for dossier in os.listdir(DATADIR): 
    total_img+= len(os.listdir(os.path.join(DATADIR,dossier)))

bar = progressbar.ProgressBar(maxval=total_img, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

def create_training_data():
    i = 0
    bar.start()
    for class_num,emotion in enumerate(EMOTIONS): 
        
        path = os.path.join(DATADIR,emotion)  
        cpt=0
        for img in os.listdir(path):
            
            try:
                img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_GRAYSCALE)  
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  
                training_data.append([new_array, class_num]) 
            except Exception as e: 
                pass

            bar.update(i)
            i+=1
        
    bar.finish()

create_training_data()
random.shuffle(training_data)

X = []
y = []

for features,label in training_data:
    X.append(features)
    m=np.zeros(7)
    m[label]=1
    y.append(m)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

pickle_out = open("data/X.pickle","wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("data/y.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()


    

