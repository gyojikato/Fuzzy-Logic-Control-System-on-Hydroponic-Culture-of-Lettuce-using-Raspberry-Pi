
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
file = open("PH.txt", 'w')

input(print("Please dip on 9.18 pH Level buffer solution and press Enter when ready."))
buf = list()
for i in range(60):
	buf.append(channel.voltage)
	print("Getting Sensor Readings...")
	time.sleep(1)
	
 
buf.sort()
buf = buf[10:50]
PH1 = round((sum(map(float, buf))/40), 2)

input(print("Please dip on 4.01 pH Level buffer solution and press Enter when ready."))
buk = list()
for i in range(60):
	buk.append(channel.voltage)
	print("Getting Sensor Readings....")
	time.sleep(1)
 
buk.sort()
buk = buk[10:50]
PH2 = round((sum(map(float, buk))/40), 2)

x = float(PH1) - float(PH2)
m = 5.17 / x
y = m * float(PH1)
b = 9.18 - y
time.sleep(10)
file.write("m="+str(m)+"\n")
file.write("b="+str(b)+"\n")
file.close()
input(print("Calibration Complete! press any key to exit."))
