import sys,cv2,os

class Webcam:

    video_capture = None

    @staticmethod
    def open():
        # set video capture device , webcam in this case
        if sys.platform == "win32":
            # video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera
            video_cap = cv2.VideoCapture(0) #captureDevice = camera
        else:
            video_cap = cv2.VideoCapture(0)

        if (not video_cap.isOpened()):
            return False       # ERROR: cannot open the webcam

        Webcam.video_capture= video_cap
        return True

        # set video capture device , webcam in this case
        # if sys.platform == "win32":
        #     Webcam.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera
        # else:
        #     Webcam.video_capture = cv2.VideoCapture(0)

        # if (not Webcam.video_capture.isOpened()):
        #     return False       # ERROR: cannot open the webcam

        # Webcam.video_capture= video_cap
        # return True


    @staticmethod    
    def take_photo(path):


        if os.path.exists(path):
            os.remove(path)

        Webcam.video_capture.set(3, 640)  # WIDTH
        Webcam.video_capture.set(4, 480)  # HEIGHT

        # save location for image
        save_loc = path

        # Capture frame-by-frame
        ret, frame = Webcam.video_capture.read()

        if (not ret):    
            return False      #ERROR: cannot open the webcam

        # mirror the frame
        frame = cv2.flip(frame, 1, 0)

        try:
            # save the detected face
            cv2.imwrite(save_loc, frame)
            os.system("chmod u+rwx "+save_loc)
        except:
            return False

        return True     #success  

    @staticmethod
    def close():
        
        # When everything is done, release the capture
        Webcam.video_capture.release()
        cv2.destroyAllWindows()

    
