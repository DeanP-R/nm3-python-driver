import time
from nm3driver import Nm3, Nm3ResponseParser
import serial

# Initialize the modems
serial_port_1 = serial.Serial('COM7', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)
left_modem = Nm3(input_stream=serial_port_1, output_stream=serial_port_1)

#serial_port_2 = serial.Serial('/dev/ttyUSB1', 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)
#right_modem = Nm3(input_stream=serial_port_2, output_stream=serial_port_2)

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

def get_address(self) -> int:
    """Gets the NM3 Address (000-255)."""

    # Absorb any incoming bytes into the receive buffers to process later
    self.poll_receiver()

    response_parser = Nm3ResponseParser()

    # Write the command to the serial port
    cmd_string = '$?'
    cmd_bytes = cmd_string.encode('utf-8')
    # Check that it has written all the bytes. Return error if not.
    if self._output_stream.write(cmd_bytes) != len(cmd_bytes):
        print('Error writing command')
        return -1

    # Await the response
    response_parser.reset()
    awaiting_response = True
    timeout_time = time.time() + Nm3.RESPONSE_TIMEOUT
    while awaiting_response and (time.time() < timeout_time):
        resp_bytes = self._input_stream.read()
        for b in resp_bytes:
            if response_parser.process(b):
                # Got a response
                awaiting_response = False
                break

    if not response_parser.has_response():
        return -1

    # Expecting '#A255V21941\r\n'
    resp_string = response_parser.get_last_response_string()
    if not resp_string or len(resp_string) < 5 or resp_string[0:2] != '#A':
        return -1

    addr_string = resp_string[2:5]
    addr_int = int(addr_string)

    return addr_int
    
print("Left Modem ", left_modem.get_address())
# print("Right Modem ", right_modem.get_address())
set_modem_address(left_modem, 255)
# set_modem_address(right_modem, 246)
