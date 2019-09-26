#! /usr/bin/env python
#
# NM V3 Logger
#
# This file is part of NM3 Python Driver. https://github.com/bensherlock/nm3-python-driver
#
#
# MIT License
#
# Copyright (c) 2019 Benjamin Sherlock <benjamin.sherlock@ncl.ac.uk>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""NM V3 Logger using the Nm3 driver. """

import argparse
import datetime
import time
import serial
from nm3driver import Nm3
from nm3driver import MessagePacket

def main():
    """Main Program Entry."""
    cmdline_parser = argparse.ArgumentParser(description='NM V3 Logger')
    
    # Add Command Line Arguments
    # Serial Port
    cmdline_parser.add_argument('port', type=string, help='The serial port to connect to the NM V3.')

    # Filename for logging
    cmdline_parser.add_argument('filename', type=string, help='The filename to log to.')
    
    # Parse the command line
    cmdline_args = cmdline_parser.parse_args()

    # Get Arguments
    port = cmdline_args.port
    filename = cmdline_args.filename
    
    # Serial Port is opened with a 100ms timeout for reading.
    serial_port = serial.Serial(port, 9600, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, 0.1)
    nm3_modem = Nm3(serial_port)

    addr = nm3_modem.get_address()
    #print('Get Address=' + '{:03d}'.format(addr))

    logfile = open(filename, 'w')
    

    # Receiving unicast and broadcast messages
    while True:
        # Periodically poll the serial port for bytes
        nm3_modem.poll_receiver()

        # Periodically process any bytes received
        nm3_modem.process_incoming_buffer()

        # Periodically check for received packets
        if nm3_modem.has_received_packet():
            message_packet = nm3_modem.get_received_packet()

            # Write to file
            # Timestamp, PacketType (Broadcast/Unicast), Source Address, Destination Address, PayloadLength, PayloadBytes(hex encoded) \r\n
            dt_str = datetime.utcnow().isoformat() + 'Z'
            logfile.write(dt_str + ',' +
                          MessagePacket.PACKETTYPE_NAMES[message_packet.packet_type] + ',' +
                          '{:03d}'.format(message_packet.source_address) + ',' +
                          '{:03d}'.format(message_packet.destination_address) + ',' +
                          '{:02d}'.format(message_packet.packet_payload.len) + ',')
                          
            for i in range(0, 64):
                if i < message_packet.packet_payload.len:
                    bytes([message_packet.packet_payload[i]]).hex() ?
                    logfile.write( '{:02d}'.format(message_packet.packet_payload[i]
            
            #payload_as_string = bytes(message_packet.packet_payload).decode('utf-8')

            #print('Received a message packet: ' +
            #      MessagePacket.PACKETTYPE_NAMES[message_packet.packet_type] +
            #      ' src: ' + str(message_packet.source_address) + ' data: ' +
            #      payload_as_string)



if __name__ == '__main__':
    main()
