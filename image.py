import cv2
import numpy as np
import math
from datetime import datetime
import onnxruntime as ort

REAL_OBJECT_WIDTH = 2.54  # cm
FOCAL_LENGTH = (250 * 30) / REAL_OBJECT_WIDTH  # pixels
IMG_HEIGHT = 2448
VERTICAL_FOV = math.degrees(2 * np.arctan2(IMG_HEIGHT / 2, FOCAL_LENGTH))  # degrees

class ObjectDetection:
    def __init__(self, camera_index=0):
        model_path = "yolotrash-v1.onnx"
        self.session = ort.InferenceSession(model_path)

        self.camera_index = camera_index
        self.video = cv2.VideoCapture(self.camera_index)
        if not self.video.isOpened():
            raise Exception("Error starting camera")


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

        original_h, original_w = frame.shape[:2]
        resized_frame = cv2.resize(frame, (412, 412))
        img = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        input_tensor = np.ascontiguousarray(img)

        outputs = self.session.run(None, {self.session.get_inputs()[0].name: input_tensor})
        detections = outputs[0][0]

        confidence_threshold = 0.5
        boxes = []
        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            if conf > confidence_threshold:
                scale_x = original_w / 412
                scale_y = original_h / 412
                x1 = int(x1 * scale_x)
                y1 = int(y1 * scale_y)
                x2 = int(x2 * scale_x)
                y2 = int(y2 * scale_y)
                boxes.append((x1, y1, x2, y2, conf, cls))

        if boxes:
            x1, y1, x2, y2, conf, cls = boxes[0]
            w, h = x2 - x1, y2 - y1
            center_x = x1 + w // 2
            dist = self.compute_distance(w)
            angle_x = self.compute_angle(center_x, original_w)
            detected_info = {
                'distance': dist,
                'angle_x': angle_x,
                'rectangle': (x1, y1, w, h),
                'center_x': center_x,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"Dist: {dist:.1f}cm, Angle: {angle_x:.1f}°"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(label)
        else:
            detected_info = None

        return frame, detected_info


    def release(self):
        self.video.release()
        cv2.destroyAllWindows()


def main():
    detector = ObjectDetection()
    try:
        while True:
            frame, detected_info = detector.detect_objects()
            if frame is not None:
                cv2.imshow("YOLO Object Detection", frame)

            key = cv2.waitKey(1)
            if key == 27:  # ESC key to break
                break
    finally:
        detector.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
