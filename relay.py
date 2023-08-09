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

Remove the Python path insert if you don't want to use it.
Need to add a try except there.
"""

import configparser
import sys
import time
sys.path.insert(3,'pyserial-3.5-py2.py3-none-any.whl')
import serial # pylint: disable=import-error,wrong-import-position


class RelayController():
    """
    Relay Controller
    """
    def __init__(self):
        self.baudrate = 9600
        self.channels = 8
        self.configfile = 'relay.conf'
        self.debug = False
        self.serialdevice = '/dev/ttyS0'
        self.config_load()

    def config_load(self):
        """
        Load config file if present
        """
        configuration = configparser.ConfigParser()
        configuration.read(self.configfile)
        if configuration['DEFAULT']['serialdevice']:
            self.serialdevice = configuration['DEFAULT']['serialdevice']
        if configuration['DEFAULT']['baudrate']:
            self.baudrate = configuration['DEFAULT']['baudrate']
        if configuration['DEFAULT']['channels']:
            self.channels = int(configuration['DEFAULT']['channels'])
        if configuration['DEFAULT']['debug']:
            self.debug = configuration['DEFAULT']['debug']
        return configuration['DEFAULT']

    def config_show(self):
        """
        Print the parsed config to the standard output
        """
        print("Show Configuration File\n")
        theconfig = self.config_load()
        for entry in theconfig:
            print("\t" + entry + ' = ' + theconfig[entry])
        print("\n")

    def channel_all_momentary(self, delay=0):
        """
        Momentary switch all channels
        """
        for channel in range(1, self.channels + 1):
            self.channel_momentary(channel)
            time.sleep(delay)

    def channel_all_off(self, delay=0):
        """
        Turn all channels off
        """
        for channel in range(1, self.channels + 1):
            self.channel_off(channel)
            time.sleep(delay)

    def channel_all_on(self, delay=0):
        """
        Turn all channels on
        """
        for channel in range(1, self.channels + 1):
            self.channel_on(channel)
            time.sleep(delay)

    def channel_all_toggle(self, delay=0):
        """
        Toggle all channels
        """
        for channel in range(1, self.channels + 1):
            self.channel_toggle(channel)
            time.sleep(delay)

    def channel_interlock(self, channel):
        """
        Set the state of a channel to on and other channels off
        This feature could be reversed on various models, test it out
        """
        command = [0x55,0x56,0,0,0,0,0,0]
        command[5] = channel
        command[6] = 5
        command[-1] = sum(command)
        self.command_send(command)
        if self.debug:
            print('Interlock channel ' + str(channel))

    def channel_momentary(self, channel):
        """
        Set the state of a channel to momentary
        on for 200ms then off
        """
        command = [0x55,0x56,0,0,0,0,0,0]
        command[5] = channel
        command[6] = 4
        command[-1] = sum(command)
        self.command_send(command)
        if self.debug:
            print('Momentary switch channel ' + str(channel))

    def channel_off(self, channel):
        """
        Set the state of a channel to off
        """
        command = [0x55,0x56,0,0,0,0,0,0]
        command[5] = channel
        command[6] = 2
        command[-1] = sum(command)
        self.command_send(command)
        if self.debug:
            print('Turn off channel ' + str(channel))

    def channel_on(self, channel):
        """
        Set the state of a channel to on
        """
        command = [0x55,0x56,0,0,0,0,0,0]
        command[5] = channel
        command[6] = 1
        command[-1] = sum(command)
        self.command_send(command)
        if self.debug:
            print('Turn on channel ' + str(channel))

    def channel_read(self, channel):
        """
        Read the state of a channel
        TODO implement some reading of the state
        Not a lot or any data on what command 0 sends back
        """
        command = [0x55,0x56,0,0,0,0,0,0]
        command[5] = channel
        command[-1] = sum(command)
        self.command_send(command)
        if self.debug:
            print('Read channel ' + str(channel))

    def command_send(self, command):
        """
        Send command to serial device
        """
        if self.debug:
            print('\tThe command is ' + str(command))
        relay = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=2)
        relay.write(command)

    def channel_toggle(self, channel):
        """
        Set the state of a channel to toggle
        """
        command = [0x55,0x56,0,0,0,0,0,0]
        command[5] = channel
        command[6] = 3
        command[-1] = sum(command)
        self.command_send(command)
        if self.debug:
            print('Toggle channel ' + str(channel))

if __name__ == '__main__':
    print(help(RelayController))
