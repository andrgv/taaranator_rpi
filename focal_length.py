import cv2

# === User Input ===
REAL_OBJECT_WIDTH = 2.54  # 1 inch in cm
KNOWN_DISTANCE = 30.0     # cm

# === Click event to capture two points ===
clicked_points = []

def click_event(event, x, y, flags, params):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Calibration Frame", frame)

        if len(clicked_points) == 2:
            pixel_width = abs(clicked_points[0][0] - clicked_points[1][0])
            focal_length = (pixel_width * KNOWN_DISTANCE) / REAL_OBJECT_WIDTH

            print("\n--- Calibration Results ---")
            print(f"Real object width: {REAL_OBJECT_WIDTH:.2f} cm (1 inch)")
            print(f"Known distance: {KNOWN_DISTANCE:.2f} cm")
            print(f"Measured pixel width: {pixel_width} px")
            print(f"Computed focal length: {focal_length:.2f} pixels")
            print("---------------------------")
            print("Use this focal length in your object detection code.")
            cv2.destroyAllWindows()

# === OpenCV webcam capture ===
cap = cv2.VideoCapture(0)  # Try 1 or 2 if 0 doesn't work
if not cap.isOpened():
    print("Error: Cannot open Arducam")
    exit()

ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Failed to grab frame from Arducam")
    exit()

cv2.imshow("Calibration Frame", frame)
cv2.setMouseCallback("Calibration Frame", click_event)
print("Click on the LEFT and RIGHT edges of the 1-inch object (at 30 cm distance) in the image window.")

cv2.waitKey(0)
cv2.destroyAllWindows()
