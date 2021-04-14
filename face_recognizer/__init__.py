import sys,os
import face_recognition
import json
from os import path


def init(path_img,path_faces,path_text,path_volume):
    extension = os.path.splitext(path_faces)[1]
    if extension==".json":
        faces = json.loads(open(path_faces).read())

        image_test = face_recognition.load_image_file(path_img)
        encoding_test = face_recognition.face_encodings(image_test)[0]
        
        to_write="0"
        # load stored images
        for face in faces['faces']:
            path_img= path_volume+'/'+face['path_img']
            if face['name'] and path.exists(path_img) and path.isfile(path_img):

                image = face_recognition.load_image_file(path_img)
                encoding = face_recognition.face_encodings(image)[0]
                result= face_recognition.compare_faces([encoding], encoding_test)[0]
                if result:
                    to_write= face['name']
                    break

        f= open(path_text, "w")
        f.write(to_write)
        f.close()

    else:
        known_image = face_recognition.load_image_file(path_faces)
        unknown_image = face_recognition.load_image_file(path_img)
        known_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        result = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
        f= open(path_text, "w")
        f.write(str(int(result)))
        f.close()


if __name__ == "__main__":
    if len(sys.argv)==5:
        init(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    else:
        print("--------------------\nface_recognizer:\n--------------------")
        print("python ./__init__.py [path_img] [path_faces] [path_text]")
        print("[path_img]: the path of the image of the face to be recognised")
        print("[path_faces]: the path of the image or the json file of images stored")
        print("[path_text]: the path of the text file in which result will be stored")
        print("[path_volume]: the path of the shared directory that this container can access\n")


# try:
#     # for testing purposes, we're just using the default API key
#     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#     # instead of `r.recognize_google(audio)`
#     print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))
