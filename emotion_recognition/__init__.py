import argparse
from webcam_utils import get_current_emotion,run_realtime_emotions
from prediction_utils import prediction_path
import sys

# for running emotion detection
def read_emotion(path):
    get_current_emotion(path)

# to run emotion detection on image saved on disk
def run_detection_path(path_img,path_text):
    prediction_path(path_img,path_text)

if __name__ == '__main__':
    if len(sys.argv)==3:
        prediction_path(sys.argv[1],sys.argv[2])
    if len(sys.argv)==4:
        prediction_path(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print("--------------------\nEmotion Recognition:\n--------------------")
        print("python ./__init__.py [path_img] [path_text]")
        print("[path_img]: the path of the image of which emotion need be detected")
        print("[path_text]: the path of the text file in which result will be stored\n")
        print("[name_model]: (optional) the name of the model to use\n")
