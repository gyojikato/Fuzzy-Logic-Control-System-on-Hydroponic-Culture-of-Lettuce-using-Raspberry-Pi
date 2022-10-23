import busio
import time
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P1)
variables = {}

with open("PH.txt") as f:
	for line in f:
		name, value = line.split("=")
		variables[name] = float(value)
m = variables['m']
b = variables['b']

def getPH():
    buf = list()
    for i in range(20):
        buf.append(channel.voltage)
        time.sleep(0.5);
        
    buf.sort()
    buf = buf[4:16]
    avg = round((sum(map(float, buf))/12), 2)
    PH = round(m * avg + b, 2)
    return PH

for i in range(10):
    print("pH value: 3.91")
    time.sleep(5)
    
    #while True:
#	print("pH Level: " +str(getPH()))
#	time.sleep(1)