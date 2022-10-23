'''!
  @file demo_read_voltage.py
  @brief connect ADS1115 I2C interface with your board (please reference board compatibility)
  @n  The voltage value read by A0 A1 A2 A3 is printed through the serial port.
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [luoyufeng](yufeng.luo@dfrobot.com)
  @version  V1.0
  @date  2019-06-19
  @url https://github.com/DFRobot/DFRobot_ADS1115
'''

import sys
sys.path.append('../')
import time

from DFRobot_ADS1115 import ADS1115
ADS1115_REG_CONFIG_PGA_6_144V        = 0x00 # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V        = 0x02 # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V        = 0x04 # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V        = 0x06 # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V        = 0x08 # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V        = 0x0A # 0.256V range = Gain 16
ads1115 = ADS1115()
variables = {}

with open("EC.txt") as f:
	for line in f:
		name, value = line.split("=")
		variables[name] = float(value)
m = variables['m']
b = variables['b']

def getEC():
	#Set the IIC address
    ads1115.set_addr_ADS1115(0x48)
    #Sets the gain and input voltage range.
    ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
    adc1 = ads1115.read_voltage(1)
    avg = adc1['r']
    EC =  round((m * avg + b), 2)
    if EC < 0:
        EC = 0;
    return EC

def getWL():
	#Set the IIC address
	ads1115.set_addr_ADS1115(0x48)
	#Sets the gain and input voltage range.
	ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
	adc2 = ads1115.read_voltage(2)
	WL = adc2['r']
	if WL < 200:
		WL = 3
	elif WL < 800:
		WL = 4
	elif WL < 1800:
		WL = 5
	else:
		WL = 6
	time.sleep(0.2)
	return WL


for i in range(10):
    print("EC value: " +str(getEC()) + "ms/cm")
    time.sleep(5)

#while True:
#	print("EC Level: " +str(getEC()))
#	time.sleep(1)