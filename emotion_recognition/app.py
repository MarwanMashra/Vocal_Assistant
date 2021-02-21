import argparse
from webcam_utils import get_current_emotion,run_realtime_emotions
from prediction_utils import prediction_path
import sys

# for running emotion detection
def read_emotion(path):
    get_current_emotion(path)

# to run emotion detection on image saved on disk
def run_detection_path(path):
    prediction_path(path)

if __name__ == '__main__':

    # read_emotion("C:/xampp/htdocs/FDS/S6/HLIN601/TER_S6/.tmp/emotion.txt")
    # run_realtime_emotions()

    if(len(sys.argv)>2 and sys.argv[2].isdigit()):
        read_emotion(sys.argv[1],int(sys.argv[2]))
    else:
        read_emotion(sys.argv[1])
