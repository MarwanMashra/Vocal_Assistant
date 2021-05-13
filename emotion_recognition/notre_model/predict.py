import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import clear_session
import numpy as np
import cv2
import sys
import random
from os.path import dirname
import os.path
import matplotlib.pyplot as plt


EMOTIONS = ['Angry', 'Disgusted', 'Fearful','Happy', 'Sad', 'Surprised', 'Neutral']
IMG_SIZE= 48

def predict(path_img):
    cv2.ocl.setUseOpenCL(False)

    # load keras model
    model = load_model('data/notre_model.h5')

    faceCascade = cv2.CascadeClassifier(r''+dirname(__file__)+'/data/haarcascades/haarcascade_frontalface_default.xml')
    # list of given emotions

    if os.path.exists(path_img):

        # read the image
        img = cv2.imread(r''+path_img, 1)

        # check if image is valid or not
        if img is None:
            print('Invalid image !!')
            return None
    else:
        print('Image not found')
        return None


    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find face in the frame
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=1,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )


    for (x, y, w, h) in faces:
        # required region for the face
        margin = 0.2
        img_face = img[int(max(0,y-h*margin)):int(y+h+h*margin), int(max(0,x-w*margin)):int(x+w+w*margin)]
        break
    try: 
        
        # remove colors
        img_face_gray = cv2.cvtColor(img_face, cv2.COLOR_BGR2GRAY)

        # resize image for the model
        img_face_gray = cv2.resize(img_face_gray, (IMG_SIZE, IMG_SIZE))
        img_face_gray = np.reshape(img_face_gray, (1, IMG_SIZE, IMG_SIZE, 1))

        # do prediction
        result = model.predict(img_face_gray)[0]
        emotion_index= np.argmax(result)

    except:
        return None

    return emotion_index

# make prediction on image saved on disk
def prediction_path(path_img,path_res):

    emotion_index = predict(path_img)
    
    if emotion_index:
        print('Detected emotion: ' + str(EMOTIONS[np.argmax(result)]))
    else:
        # No face detected
        emotion_index= str(-1)

    if path_res and os.path.exists(path_res) and os.path.isfile(path_res):
        f= open(path_res,"w")
        f.write(str(emotion_index))
        f.close()
        
    return



