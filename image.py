import cv2
import numpy as np
import math

#TODO: for now, the "trash" objects are going to be the extra blocks i printed by accident
#TODO: actually make the model, have to take a bunch of photos with full system D:
model = cv2.CascadeClassifier('cascade.xml')

REAL_OBJECT_WIDTH = 5 # cm. TODO: is it though?
FOCAL_LENGTH = 700 # pixels. TODO: is it though?
HORIZONTAL_FOV = 60 # degrees. TODO: is it though?

log_file = open()

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        # no longer there
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    objects = model.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in objects:
        # draw a rectangle around the detected object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        center_x = x + w // 2
        center_y = y + h // 2

        if w != 0:
            distance = (FOCAL_LENGTH * REAL_OBJECT_WIDTH) / w
            print(f"Distance: {distance:.2f} cm")
        else:
            distance = float('inf')

        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2

        angle_x = math.degrees(math.atan2(center_x - frame_center_x, FOCAL_LENGTH))
        loc_info = f"Distance: {distance:.2f} cm, Angle: {angle_x:.2f} degrees"
        cv2.putText(frame, loc_info, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        print(loc_info)

    cv2.imshow('Frame', frame)

    # break if q is pressed. TODO: put a physical stop to the system
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()