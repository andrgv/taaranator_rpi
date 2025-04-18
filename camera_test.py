import cv2

print("Searching for available camera indices...")

for index in range(10):  # Try indices 0 through 9
    cap = cv2.VideoCapture(index)
    if cap.read()[0]:
        print(f"Camera found at index {index}")
        cap.release()
    else:
        print(f"No camera at index {index}")