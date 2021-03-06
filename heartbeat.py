#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Blinks an LED in a heartbeat style"""

from __future__ import print_function
import time
import RPi.GPIO as GPIO

PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, 0)

while 1:
    try:
        GPIO.output(PIN, 1)
        time.sleep(0.2)
        GPIO.output(PIN, 0)
        time.sleep(0.2)
        GPIO.output(PIN, 1)
        time.sleep(0.2)
        GPIO.output(PIN, 0)
        time.sleep(1.1)
    except KeyboardInterrupt:
        break

GPIO.cleanup()
print('GPIO cleanup done!')
