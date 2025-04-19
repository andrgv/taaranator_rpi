import cv2
import time
from spi import SPI
from motor import Motor
from image import ObjectDetection
from core.enums import Command
from core.enums import Mode
from core.logger import setup_logger

DISTANCE_THRESHOLD = 5 # cm TODO: change, these are just placeholders now
ANGLE_THRESHOLD = 10 # degrees
WALL_DISTANCE_THRESHOLD = 20 # cm


def main():
    #Setup logger
    logger = setup_logger(__name__)

    # Initialize SPI interface
    spi_interface = SPI(0, 0, 500000)
    logger.info("SPI initialized")
    motor = Motor(spi_interface)
    logger.info("Motors initialized")
    object_detection = ObjectDetection(camera_index=0)
    logger.info("Object detection initialized")

    current_mode = Mode.AIMLESS

    try:
        while True:
            match current_mode:
                case Mode.AIMLESS:
                    motor.move_forward()
                    frame, detection = object_detection.detect_objects()
                    if detection:
                        logger.info(f"{detection['time']}: Detected object at distance {detection['distance']} cm, angle {detection['angle_x']} degrees")
                        current_mode = Mode.TRASH_DETECTED
                case Mode.TRASH_DETECTED:
                    frame, detection = object_detection.detect_objects()
                    if detection:
                        if detection['distance'] < DISTANCE_THRESHOLD:
                            logger.info("Trash collected. Switching to BROOMING_AWAY mode")
                            motor.stop()
                            current_mode = Mode.BROOMING_AWAY
                        else:
                            if detection['angle_x'] > ANGLE_THRESHOLD:
                                logger.info("Rotating left towards trash")
                                motor.move_left()
                            elif detection['angle_x'] < -ANGLE_THRESHOLD:
                                logger.info("Rotating left towards trash")
                                motor.move_right()
                            else:
                                logger.info("Moving forward towards trash")
                                motor.move_forward()
                    else:
                        logger.info("Lost track of object, reutrning to AIMLESS mode")
                        current_mode = Mode.AIMLESS
                case Mode.BROOMING_AWAY:
                    sensor_distance = spi_interface.send_command(Command.SENSOR.value)
                    logger.info("Ultrasonic sensor distance: {sensor_distance} cm")
                    if sensor_distance <= WALL_DISTANCE_THRESHOLD:
                        logger.info("Wall reached, dropping off trash and switching to AIMLESS")
                        motor.stop()
                        motor.move_reverse()
                        motor.move_left()
                        current_mode = Mode.AIMLESS
                    else:
                        logger.info("Moving forward to drop off trash")
                        motor.move_forward()

            if current_mode in (Mode.AIMLESS, Mode.TRASH_DETECTED) and frame is not None:
                cv2.imshow('Camera Feed', frame)
            # TODO: turn keyboard interrupt to button interrupt
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.1) #TODO: might have to change this delay

    except KeyboardInterrupt:
        logger.info("Stopping program")
    finally:
        motor.stop()
        object_detection.release()
        spi_interface.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()