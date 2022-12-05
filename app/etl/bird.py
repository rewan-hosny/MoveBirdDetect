import cv2
import pandas as pd
import numpy as np
from app.etl.tracker import *
class birds :
    def pega_center(x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return cx, cy
    def count_birds(videoPath):
        ww = 80
        offset = 6
        y1 = 360
        delay = 60
        count = 0




        cap = cv2.VideoCapture(videoPath)


        # Create tracker object
        tracker = EuclideanDistTracker()

        # Object detection from Stable camera
        object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

        while True:
            ret, frame = cap.read()
            ret, frame = cap.read()
            #height, width, _ = frame.shape
            if frame is None:
                break
            #print(height, width)
            # 1. Object Detection
            mask = object_detector.apply(frame)
            _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
            # dilat=cv2.dilate(mask,np.ones((5,5)))

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.line(frame, (560, 0), (560, 720), (255, 0, 0), 2)
            detections = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 100:
                    # cv2.drawContours(frame,[cnt],-1,(75,0,130),2)
                    x, y, w, h = cv2.boundingRect(cnt)
                    # cv2.rectangle(frame,(x,y),(x+w,y+h),(75,0,130),3)
                    validator_contorno = (x >= ww)
                    if not validator_contorno:
                        continue
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    center = birds.pega_center(x, y, w, h)
                    detections.append(center)
                    cv2.circle(frame, center, 4, (75, 0, 130), -1)

                    for (x, y) in detections:
                        if (x < (y1 + offset) and x > (y1 - offset)):
                            count += 1
                            cv2.line(frame, (560, 0), (560, 720), (75, 0, 130), 2)
                            detections.remove((x, y))
                            print("Number of birds detected :" + str(count))

                    cv2.putText(frame, "birds count : " + str(count), (60, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 4)


            cv2.imshow("Frame", frame)
            cv2.imshow("Mask", mask)


            key = cv2.waitKey(27)
            if key == 27:
                break
        print("total count :",count)
        data = {'count': [count]}

        df = pd.DataFrame (data)


        return df

