import os,time

def abspath(file):
    return os.path.abspath(os.path.dirname(file))+"/"

def watch(path_file,t,wait=10):
    if wait>100:
        print("ERROR: wait should be < 100")
        return False

    while True:   # wait for the result of emotion_recognition

        # result came out 
        if (os.path.isfile(path_file) and (os.stat(path_file)[8] >= t)):   
            return True

        # time out and no result yet
        if (time.time() > t+wait):
            print("Timeout")
            return False
