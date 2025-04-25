from core.enums import Command
import time

class Motor:
    ANGULAR_VELOCITY_DEG_PER_SEC = 45

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
    
    def move_left(self, angle_deg=None):
        duration = angle_deg / self.ANGULAR_VELOCITY_DEG_PER_SEC if angle_deg else None
        response = self.spi_interface.send_command(Command.LEFT.value)
        if angle_deg:
            time.sleep(duration)
            self.stop()
        return response
    
    def move_right(self, angle_deg=None):
        duration = angle_deg / self.ANGULAR_VELOCITY_DEG_PER_SEC if angle_deg else None
        response = self.spi_interface.send_command(Command.RIGHT.value)
        if angle_deg:
            time.sleep(duration)
            self.stop()
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

        motor.move_left()
        time.sleep(1)

        motor.move_right()
        time.sleep(1)

        motor.stop()

        sensor_value = motor.sensor()
        print(f"Sensor value: {sensor_value}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        spi_interface.close()