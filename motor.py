# from core.enums import Command

# class Motor:
#     def __init__(self, spi_interface):
#         self.spi_interface = spi_interface

#     def move_forward(self):
#         response = self.spi_interface.send_command(Command.FORWARD.value)
#         if response != 0:
#             raise Exception("Error moving forward")
#         return response
    
#     def move_reverse(self):
#         response = self.spi_interface.send_command(Command.BACK.value)
#         if response != 0:
#             raise Exception("Error moving reverse")
#         return response
    
#     def move_left(self):
#         response = self.spi_interface.send_command(Command.LEFT.value)
#         if response != 0:
#             raise Exception("Error moving left")
#         return response
    
#     def move_right(self):
#         response = self.spi_interface.send_command(Command.RIGHT.value)
#         if response != 0:
#             raise Exception("Error moving right")
#         return response
    
#     def stop(self):
#         response = self.spi_interface.send_command(Command.STOP.value)
#         if response != 0:
#             raise Exception("Error stopping")
#         return response
    
#     def sensor(self):
#         response = self.spi_interface.send_command(Command.SENSOR.value)
#         if response == 0:
#             raise Exception("Error reading sensor")
#         return response
    
# def main():
#     import time
#     from spi import SPI

#     spi_interface = SPI(0, 0, 500000)
#     motor = Motor(spi_interface)
#     try:
#         motor.move_forward()
#         time.sleep(1)

#         motor.move_reverse()
#         time.sleep(1)

#         motor.move_left()
#         time.sleep(1)

#         motor.move_right()
#         time.sleep(1)

#         motor.stop()

#         sensor_value = motor.sensor()
#         print(f"Sensor value: {sensor_value}")

#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         spi_interface.close()

from core.enums import Command
import time  # Added to support timing in rotation methods

class Motor:
    ANGULAR_VELOCITY_DEG_PER_SEC = 45  # Adjust this after calibration

    def __init__(self, spi_interface):
        self.spi_interface = spi_interface

    def move_forward(self):
        response = self.spi_interface.send_command(Command.FORWARD.value)
        if response != 0:
            raise Exception("Error moving forward")
        return response

    def move_reverse(self):
        response = self.spi_interface.send_command(Command.BACK.value)
        if response != 0:
            raise Exception("Error moving reverse")
        return response

    def move_left(self):
        response = self.spi_interface.send_command(Command.LEFT.value)
        if response != 0:
            raise Exception("Error moving left")
        return response

    def move_right(self):
        response = self.spi_interface.send_command(Command.RIGHT.value)
        if response != 0:
            raise Exception("Error moving right")
        return response

    def stop(self):
        response = self.spi_interface.send_command(Command.STOP.value)
        if response != 0:
            raise Exception("Error stopping")
        return response

    def sensor(self):
        response = self.spi_interface.send_command(Command.SENSOR.value)
        if response == 0:
            raise Exception("Error reading sensor")
        return response

    def rotate_left_by_angle(self, angle_deg=None):
        if angle_deg is None:
            angle_deg = 90
        duration = angle_deg / self.ANGULAR_VELOCITY_DEG_PER_SEC
        self.move_left()
        time.sleep(duration)
        self.stop()

    def rotate_right_by_angle(self, angle_deg=None):
        if angle_deg is None:
            angle_deg = 90
        duration = angle_deg / self.ANGULAR_VELOCITY_DEG_PER_SEC
        self.move_right()
        time.sleep(duration)
        self.stop()

def main():
    import time
    from spi import SPI

    spi_interface = SPI(0, 0, 500000)
    motor = Motor(spi_interface)
    try:
        motor.move_forward()
        time.sleep(1)

        motor.move_reverse()
        time.sleep(1)

        motor.rotate_left_by_angle()       # Default 90°
        time.sleep(1)

        motor.rotate_right_by_angle(45)    # Custom 45°

        motor.stop()

        sensor_value = motor.sensor()
        print(f"Sensor value: {sensor_value}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        spi_interface.close()