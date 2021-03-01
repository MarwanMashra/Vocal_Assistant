import sys,cv2

class Webcam:

    def __init__(self):
        self.video_capture = None

    def open(self):
        # set video capture device , webcam in this case
        if sys.platform == "win32":
            video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera
        else:
            video_cap = cv2.VideoCapture(0)

        if (not video_cap.isOpened()):
            return False       # ERROR: cannot open the webcam

        self.video_capture= video_cap
        return True

        
    def take_photo(self,path):

        self.video_capture.set(3, 640)  # WIDTH
        self.video_capture.set(4, 480)  # HEIGHT

        # save location for image
        save_loc = path+"/face.jpg"

        # Capture frame-by-frame
        ret, frame = self.video_capture.read()

        if (not ret):    
            return False      #ERROR: cannot open the webcam

        # mirror the frame
        frame = cv2.flip(frame, 1, 0)

        try:
            # save the detected face
            cv2.imwrite(save_loc, frame)
        except:
            return False

        return True     #success  


    def close(self):
        
        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

    
