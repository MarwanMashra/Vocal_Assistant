from model_utils import define_model, model_weights
import cv2
import os.path
import numpy as np
from os.path import dirname

# make prediction on image saved on disk
def prediction_path(path_img,path_res):
    # load keras model
    model = define_model()
    model = model_weights(model)

    faceCascade = cv2.CascadeClassifier(r''+dirname(__file__)+'/haarcascades/haarcascade_frontalface_default.xml')
    # list of given emotions
    EMOTIONS = ['Angry', 'Disgusted', 'Fearful',
                'Happy', 'Sad', 'Surprised', 'Neutral']

    if os.path.exists(path_img):
        # read the image
        # print(path)
        img = cv2.imread(r''+path_img, 1)
        # print(img)
        # check if image is valid or not
        if img is None:
            print('Invalid image !!')
            return 
    else:
        print('Image not found')
        return

    # print("######################")
    # print(img)
    
    # window_name = 'Image'
    # Displaying the image 
    # cv2.imshow(window_name, img) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow(window_name, gray) 
    # cv2.waitKey(3000)

    # find face in the frame
    faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

    for (x, y, w, h) in faces:
        # required region for the face
        img_face = img[y-90:y+h+70, x-50:x+w+50]
        print(x, y, w, h)
        break
    
    try: 
        # remove colors
        img_face_gray = cv2.cvtColor(img_face, cv2.COLOR_BGR2GRAY)
        # resize image for the model
        img_face_gray = cv2.resize(img_face_gray, (48, 48))
        img_face_gray = np.reshape(img_face_gray, (1, 48, 48, 1))
        # do prediction
        result = model.predict(img_face_gray)
        # print emotion
        print('Detected emotion: ' + str(EMOTIONS[np.argmax(result[0])]))
    except:
        # No face detected
        return
    
    # show image
    # cv2.imshow("Image", img_face) 
    # cv2.waitKey(0)

    f= open(path_res,"w")
    f.write(str(np.argmax(result[0])))
    f.close()

    return
