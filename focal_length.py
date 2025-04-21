import cv2

# Constants
REAL_OBJECT_WIDTH = 2.54  # cm (1 inch)
KNOWN_DISTANCE = 30.0     # cm

# Open Arducam (USB)
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access Arducam")
    exit()

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read frame")
    exit()

# Save the image to file
cv2.imwrite("frame.jpg", frame)
print("Image saved as 'frame.jpg'")
print("Use SCP or SFTP to download the image and open it on your laptop.")
print("Measure the object's pixel width (left-to-right) in any image viewer.")
print("Then use the formula below to compute the focal length:")
print()
print("    focal_length = (pixel_width * known_distance) / real_width")
print(f"With known_distance = {KNOWN_DISTANCE} cm, real_width = {REAL_OBJECT_WIDTH} cm")
