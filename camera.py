import cv2
import time
from datetime import datetime
import os

# Initialize the video capture object (0 is usually /dev/video0)
cap = cv2.VideoCapture(13)

if not cap.isOpened():
    print("Failed to open the camera.")
    exit()

os.makedirs("data", exist_ok=True)

# Optional: Set resolution TODO: find actual resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

print("Starting image capture every 5 seconds. Press Ctrl+C to stop.")

try:
    while True:
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captured {filename}")
        else:
            print("Failed to capture image.")
        
        time.sleep(5)

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    cap.release()
    print("Camera released.")
