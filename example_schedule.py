#!/usr/bin/env python3
"""
Serial relay example with schedule

Assuming:
* exterior lights are on channel 1
* vent fan is on channel 2
* sprinkler_one is on channel 3
* router is on channel 4

These are very simple and silly. More logic or process could be used.
"""

import sys
import time
from relay import RelayController
try:
    sys.path.insert(3, 'schedule-1.2.0-py2.py3-none-any.whl')
    import schedule # pylint: disable=import-error,wrong-import-position
except ImportError:
    import schedule

def exterior_lights(operation):
    """
    Manage exterior lights
    """
    myrelay = RelayController()
    print("Manage exterior lights. Operation: " + operation)
    myrelay.channel_operation(1, operation)

def vent_fan(delay):
    """
    Manage vent fan
    """
    myrelay = RelayController()
    print("Manage vent fan")
    myrelay.channel_operation(2, 'on')
    time.sleep(int(delay))
    myrelay.channel_operation(2, 'off')

def sprinkler_one(operation):
    """
    Control the sprinkler
    """
    myrelay = RelayController()
    print("Manage sprinkler_one")
    myrelay.channel_operation(3, operation)

def reboot_router(delay=10):
    """
    reboot the router
    """
    myrelay = RelayController()
    print("Reboot the router with a delay")
    myrelay.channel_operation(4, 'off')
    time.sleep(delay)
    myrelay.channel_operation(4, 'on')

if __name__ == '__main__':
    schedule.every().hour.do(vent_fan, 300)
    schedule.every().day.at("23:40").do(reboot_router, delay=11)
    schedule.every().day.at("20:30").do(exterior_lights, 'on')
    schedule.every().day.at("06:30").do(exterior_lights, 'off')
    schedule.every().day.at("05:15").do(sprinkler_one, 'on')
    schedule.every().day.at("05:20").do(sprinkler_one, 'off')
    try:
        print("Use control + c to exit\n\n")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nThanks for playing with relays and schedule")
