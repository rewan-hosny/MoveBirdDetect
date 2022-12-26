from queue import Queue
import cv2 as cv 
from threading import Thread

class Predictor(object,Thread):
    def __init__(self,model_path , video , queue):
        self.model = model_path
        self.Video = video 
        self.queue = queue
        # TODO : unpickle the class names of the model from the model path.
        # self.class_names = 


    def run(self):
        video_stream = cv.VideoCapture(self.Video)
        

        frame_number = 0

        while video_stream.isOpen():
            ret , frame = video_stream.read() 
            frame_number += 1
            Bird_Pose = {"head":"left" , "leg":"down" , "wing":"on" , "tail":"center"}     # self.model.predict([frame])
            self.queue.put((Bird_Pose , frame_number ))
        
        self.queue.put((None,None))
        


