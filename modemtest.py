from nm3driver import NM3
import serial

# Initialize the modems
serial_port_1 = serial.Serial('/dev/ttyUSB0', 9600)
left_modem = NM3(serial_port=serial_port_1)

serial_port_2 = serial.Serial('/dev/ttyUSB1', 9600)
right_modem = NM3(serial_port=serial_port_2)
