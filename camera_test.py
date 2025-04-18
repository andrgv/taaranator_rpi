import cv2

print("Testing available video devices...\n")
for i in range(32):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    print(f"/dev/video{i} opened: {cap.isOpened()}, frame captured: {ret}")
    cap.release()