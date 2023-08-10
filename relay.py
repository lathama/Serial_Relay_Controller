#!/usr/bin/env python
"""
Serial Relay Controller

Several makes of multi channel relay boards that are controlled over an RS232
serial port. I am testing with a model that uses a ULN2803A chip also noted as
a `darlington array` and an RS232 level shifter chip that is hard to read the
label on.

Other labels silkscreened on the board:
`R221A08`
`8 Channel RS232 Relay`
`eletechsup`

Control Commands
0 - Read
1 - Open
2 - Close
3 - Toggle
4 - Momentary ~200ms
5 - Interlock

Add user to dialout group for access to ttyS or ttyUSB devices
"""

import argparse
import os
from stat import S_ISCHR
import sys
import time
try:
    sys.path.insert(3, 'pyserial-3.5-py2.py3-none-any.whl')
    import serial # pylint: disable=import-error,wrong-import-position
except ImportError:
    import serial

DEBUG = False

class RelayController():
    """
    Relay Controller
    """
    def __init__(
        self,
        device: str = '/dev/ttyUSB0',
        baud: int = 9600,
        channels: int = 4):
        self.conf = {
            'baud': baud,
            'channels': channels,
            'device': device}
        self.operations = {
            'on': 1,
            'off': 2,
            'toggle': 3,
            'momentary': 4,
            'interlock': 5}
        self.check_device()

    def channel_operation(self, channel: int = 1, operation: str = 'off'):
        """
        Operate on a single channel
        """
        cmd = [0x55, 0x56, 0, 0, 0, channel, self.operations[operation], 0]
        cmd[-1] = sum(cmd)
        self.command_send(cmd)
        print("Channel " + str(channel) + " sent operation: " + operation)

    def channel_operation_all(self, operation: str = 'off', delay: int = 0):
        """
        Operate on a all channels
        """
        for channel in range(1, self.conf['channels'] + 1):
            self.channel_operation(channel, operation)
            time.sleep(delay)

    def check_device(self):
        """
        Check that the serial device exists and the user has perms
        This cold be done better
        """
        try:
            device = os.stat(self.conf['device']).st_mode
            if not S_ISCHR(device):
                print("Device not found")
                sys.exit()
        except FileNotFoundError:
            print("Device not found")
            sys.exit()
        if not os.access(self.conf['device'], os.W_OK):
            print("User lacks permission for device")
            sys.exit()

    def command_send(self, command: list):
        """
        Send command to serial device
        """
        if DEBUG:
            print("\tThe command is " + str(command))
        relay = serial.Serial(
            self.conf['device'], baudrate=self.conf['baud'], timeout=1)
        relay.write(command)

if __name__ == '__main__':
    cli = argparse.ArgumentParser(
        description='Serial Relay Controller',
        prog='Serial Relay Controller',
        epilog='by Andrew lathama Latham')
    groupa = cli.add_mutually_exclusive_group(required=True)
    groupa.add_argument(
        '-a', '--all',
        action='store_true',
        help='Select All Channels',
        dest="all")
    groupa.add_argument(
        '-c', '--channel',
        action='store',
        type=int,
        choices=range(1, 17),
        help='Select Channel',
        dest="channel")
    cli.add_argument(
        '-o', '--operation',
        action='store',
        type=str,
        choices=['on', 'off', 'toggle', 'interlock', 'momentary'],
        help='Select Operation to Perform',
        dest="operation")
    cli.add_argument(
        '-b', '--baud',
        action='store',
        default=9600,
        type=int,
        help='Select Baud Rate. Defaults to 9600',
        dest='baud')
    cli.add_argument(
        '-d', '--device',
        action='store',
        default='/dev/ttyUSB0',
        type=str,
        help='Select a Serial Device. Defaults to /dev/ttyUSB0',
        dest='device')
    cli.add_argument(
        '-n', '--number',
        action='store',
        default=4,
        type=int,
        choices=range(1, 17),
        help='Select Number of Channels. Defaults to 4',
        dest="channels")
    cli.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show debug info',
        dest="verbose")
    cli_entries = cli.parse_args(args=None if sys.argv[1:] else ['--help'])
    if cli_entries.verbose:
        DEBUG = True
    if cli_entries.channel and cli_entries.operation:
        relay_single = RelayController(device=cli_entries.device)
        relay_single.channel_operation(cli_entries.channel, cli_entries.operation)
    if cli_entries.all and cli_entries.operation:
        relay_all = RelayController(device=cli_entries.device, channels=cli_entries.channels)
        relay_all.channel_operation_all(cli_entries.operation)
