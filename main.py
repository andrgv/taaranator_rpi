import cv2
import time
from spi import SPI
from motor import Motor
from image import ObjectDetection
from core.enums import Command

DISTANCE_THRESHOLD = 10 # cm TODO: change, these are just placeholders now
ANGLE_THRESHOLD = 10 # degrees

# TODO: only trash detection mode now, need to implement trash deposition and mode switching
def main():
    # Initialize SPI interface
    spi_interface = SPI(0, 0, 500000)
    motor = Motor(spi_interface)
    object_detection = ObjectDetection(camera_index=0)

    try:
        while True:
            frame, detection = object_detection.detect_objects()
            if frame is None:
                print("Error capturing frame")
                continue

            if detection is not None:
                print(f"{detection['time']}: Detected object at distance {detection['distance']} cm, angle {detection['angle_x']} degrees")

                if detection['distance'] < DISTANCE_THRESHOLD:
                    if abs(detection['angle_x']) > ANGLE_THRESHOLD:
                        if detection['angle_x'] > 0:
                            motor.move_right()
                        else:
                            motor.move_left()
                    else:
                        motor.stop()
                        print("Stopping, object is close enough")
                
                cv2.imshow("Object Detection", frame)
                # This is just a keyboard stop, we might want to change it a physical button
                if cv2.waitKey(1) & 0xFF == ord('q'): 
                    break

                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping program")
    finally:
        motor.stop()
        object_detection.release()
        spi_interface.close()
        cv2.destroyAllWindows()