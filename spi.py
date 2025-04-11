import spidev
import time
from core.enums import Command

class SPI:
    def __init__(self, bus=0, device=0, max_speed_hz=500000): # TODO: check speed is ok
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = 0b00
        self.spi.bits_per_word = 8
        #  TODO: I don't think I need to set these defaults...
        # self.spi.cshigh = False
        # self.spi.lsbfirst = False
        # self.spi.no_cs = False
    
    def send_command(self, command):
        char_to_send = ord(command)
        response = self.spi.xfer2([char_to_send])
        return response[0]
    
    def close(self):
        self.spi.close()
    
def main():
   # Main function for testing purposes, will not actually run in actual system
    spi_interface = SPI(0, 0, 500000) 
    try:
        #send sendor command
        sensor = spi_interface.send_command(Command.SENSOR.value)
        print(f"Sensor response: {sensor}") # should > 0

        #send move forward
        forward = spi_interface.send_command(Command.FORWARD.value)
        print(f"Move forward response: {forward}") # should be 0. TODO: if time write actual tests
        time.sleep(1) # should move for 1 sec

        #send move reverse
        reverse = spi_interface.send_command(Command.BACK.value)
        print(f"Move reverse response: {reverse}") # should be 0.
        time.sleep(1) # should move for 1 sec

        #send move left
        left = spi_interface.send_command(Command.LEFT.value)
        print(f"Move left response: {left}") # should be 0.
        time.sleep(1) # should move for 1 sec
        
        #send move right
        right = spi_interface.send_command(Command.RIGHT.value)
        print(f"Move right response: {right}") # should be 0.
        time.sleep(1) # should move for 1 sec
        
        #send stop
        stop = spi_interface.send_command(Command.STOP.value)
        print(f"Stop response: {stop}") # should be 0.

    except Exception as e:
        # handle errors in data transmission
        print(f"Error in SPI communication: {e}")
    finally:
        spi_interface.close()

if __name__ == "__main__":
    main()