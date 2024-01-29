import time
from nm3driver import Nm3
import serial

# Initialize the modems
serial_port_1 = serial.Serial('/dev/ttyUSB0', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)
left_modem = Nm3(input_stream=serial_port_1, output_stream=serial_port_1)

serial_port_2 = serial.Serial('/dev/ttyUSB1', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)
right_modem = Nm3(input_stream=serial_port_2, output_stream=serial_port_2)

def set_modem_address(modem, address):
    if modem:
        try:
            result = modem.set_address(address)
            if result == address:
                print(f"Address set to {address} on modem.")
            else:
                print(f"Failed to set address on modem. Response: {result}")
        except Exception as e:
            print(f"Error setting address on modem: {e}")


set_modem_address(left_modem, 123)
set_modem_address(right_modem, 246)
