#!/usr/bin/env python3
"""
Serial relay example turns on all channels with delay then off with delay
"""

import time
from relay import RelayController

if __name__ == '__main__':
    myrelay = RelayController()
    myrelay.debug = True
    print("\nTurn on all channels\n")
    myrelay.channel_all_on(1)
    print("\nWaiting a few seconds\n")
    time.sleep(3)
    print("Turn all the channels off\n")
    myrelay.channel_all_off(1)
    print("\nThanks for using this example\n")
