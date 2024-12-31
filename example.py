#!/usr/bin/env python3
"""
Serial relay example turns on all channels with delay then off with delay
"""

import sys
import time
from relay import RelayController
sys.dont_write_bytecode = True

if __name__ == '__main__':
    myrelay = RelayController(
        device = '/dev/ttyUSB0',
        baud = 9600,
        channels = 8)
    myrelay.debug = True
    print("\nTurn on all channels\n")
    myrelay.channel_operation_all('on')
    print("\nWaiting a few seconds\n")
    time.sleep(3)
    print("Turn all the channels off\n")
    myrelay.channel_operation_all('off')
    print("\nThanks for using this example\n")
