#!/usr/bin/python3
# sample
#print(matrix[3][0])
import pprint
import board
import busio
from digitalio import Direction
from time import sleep
from yahoo_fin.stock_info import get_live_price
from yahoo_fin.stock_info import get_quote_table

from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

pp = pprint.PrettyPrinter(indent=4)

mcp = MCP23017(i2c)

pins_matrix = [[5,6],
          [7,3],
          [1,2],
          [4,0]]

all_off = [[0,0],
           [0,0],
           [0,0],
           [0,0]]

all_on = [[1,1],
          [1,1],
          [1,1],
          [1,1]]

stock_mx = [[0,0],
           [0,0],
           [0,0],
           [0,0]]

pins = {}
def setup_pins():
    # setup pins for output to LED
    print("Pin setup")
    for x in range(0,8):
        pins[x]=mcp.get_pin(x)
        pins[x].direction = Direction.OUTPUT

def write_mx(write_matrix):
    for row in pins_matrix:
        # lookup the pins
        left = row[0]
        right = row[1]
        index = pins_matrix.index(row)
        print("index is " + str(index))
        print("pins to write are " + str(left) + str(right))
        print("----")
        print("values to write are")
        new_left = write_matrix[index][0]
        new_right = write_matrix[index][1]
        print(new_left,new_right)
        print("left is" + str(left))
        pins[left].value = new_left
        pins[right].value = new_right

def check_stock(stock,row):
    print("check_stock->" + stock)
    print("will update row->" + str(row))
    try:
        price = get_live_price(stock)
    except:
        stock_mx[row][0] = 0
        stock_mx[row][1] = 0
        return
    try:
        prev_price = get_quote_table(stock)['Previous Close']
    except:
        stock_mx[row][0] = 0
        stock_mx[row][1] = 0
    
    if price > prev_price:
        print(stock + " up")
        stock_mx[row][0] = 0
        stock_mx[row][1] = 1
        return(True)
    else:
        print(stock + " down")
        stock_mx[row][0] = 1
        stock_mx[row][1] = 0
        return(False)

def flash(times):
    for x in range(0,times):
        print("Flashing leds")
        write_mx(all_on)
        sleep(.3)
        write_mx(all_off)
        sleep(.3)

# --------- main loop -------------
setup_pins()
write_mx(all_off)
flash(2)
while True:
    check_stock("fds",0)
    check_stock("^dji",1)
    check_stock("efa",2)
    check_stock("agg",3)
    print(stock_mx)
    flash(3)
    write_mx(stock_mx)
    sleep(10)
