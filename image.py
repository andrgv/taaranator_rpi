import cv2
import numpy as np
import math
from datetime import datetime

#TODO: for now, the "trash" objects are going to be the extra blocks i printed by accident
#TODO: actually make the model, have to take a bunch of photos with full system D:
model = cv2.CascadeClassifier('cascade.xml')

REAL_OBJECT_WIDTH = 5 # cm. TODO: is it though?
FOCAL_LENGTH = 700 # pixels. TODO: is it though?
HORIZONTAL_FOV = 60 # degrees. TODO: is it though?

class ObjectDetection:
    def __init__(self, camera_index=0):
        self.cascade = cv2.CascadeClassifier('cascade.xml')
        if self.cascade.empty():
            raise Exception("Error loading cascade classifier")
        self.camera_index = camera_index
        self.video = cv2.VideoCapture(self.camera_index)
        if not self.video.isOpened():
            raise Exception("Error staring camera")
        
    def compute_distance(self, width):
        if width == 0:
            return float('inf')
        return (FOCAL_LENGTH * REAL_OBJECT_WIDTH) / width
    
    def compute_angle(self, center_x, frame_width):
        frame_center_x = frame_width // 2
        angle_x = math.degrees(math.atan2(center_x - frame_center_x, FOCAL_LENGTH))
        return angle_x

    def detect_objects(self):
        ret, frame = self.video.read()
        if not ret:
            return None, None
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        objects = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(objects) > 0:
            x, y, w, h = objects[0]  # we only care about the first detected object
            center_x = x + w // 2
            dist =self.compute_distance(w)
            angle_x = self.compute_angle(center_x, frame.shape[1])
            detected_info = {
                'distance': dist,
                'angle_x': angle_x,
                'rectangle': (x, y, w, h),
                'center_x': center_x,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            loc_info = f"Distance: {dist:.2f} cm, Angle: {angle_x:.2f} degrees"
            cv2.putText(frame, loc_info, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(loc_info)
        else:
            detected_info = None
        return frame, detected_info
    
    def release(self):
        self.video.release()
        cv2.destroyAllWindows()