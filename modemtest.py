from nm3driver import NM3
import serial

# Initialize the modems
serial_port_1 = serial.Serial('/dev/ttyUSB0', 9600)
modem1 = NM3(serial_port=serial_port_1)

serial_port_2 = serial.Serial('/dev/ttyUSB1', 9600)
modem2 = NM3(serial_port=serial_port_2)

# Set addresses
# The exact method to set the address depends on the functions provided by the driver
# For example, it might be something like:
modem1.set_address(1)
modem2.set_address(2)

# Your code to interact with the modems
# ...

# Close the serial ports
serial_port_1.close()
serial_port_2.close()
