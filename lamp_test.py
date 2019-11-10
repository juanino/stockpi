#!/usr/bin/python3
#print(matrix[3][0])
import pprint
import board
import busio
from digitalio import Direction
from time import sleep

from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

pp = pprint.PrettyPrinter(indent=4)

mcp = MCP23017(i2c)

matrix = [[5,6],
          [7,3],
          [1,2],
          [4,0]]

# setup pins for output to LED
print("Pin setup")
pins = {}
for x in range(0,8):
    pins[x]=mcp.get_pin(x)
    pins[x].direction = Direction.OUTPUT

# clear all LEDs to off
print("Clearing all LEDs")
for x in range(0,8):
    pins[x].value = False
    print(x, pins[x].value)
    sleep(.1)

print("Turn on row at a time")
input("press enter:")

# walk each light
for row in matrix:
    print(row)
    left = (row[0])
    right = (row[1])
    pins[left].value = True
    sleep(.3)
    pins[right].value = True
    sleep(.5)

print("Clear all LEDs")
input("press enter:")

for x in range(0,8):
    pins[x].value = False
    print(x, pins[x].value)
    sleep(.1)

# manual one by one
print("One by one test")
for x in range(0,8):
    input("press enter:")
    pins[x].value = True
    print(x, pins[x].value)
    sleep(.1)

print("Clear all LEDs")
for x in range(0,8):
    pins[x].value = False
    print(x, pins[x].value)
    sleep(.1)

print("flash")
input("press enter:")
for x in range(0,3):
    for x in range(0,8):
        pins[x].value = True
        print(x, pins[x].value)
    sleep(.4)
    for x in range(0,8):
        pins[x].value = False
        print(x, pins[x].value)
    sleep(2)

sleep(1)

# the old twinkle loop
print("twinkle")
input("press enter:")
for x in range(0,3):
    for x in range(0,8):
        pins[x].value = True
        print(x, pins[x].value)
        sleep(.1)
        pins[x].value = False
        sleep(.1)

print("end")
