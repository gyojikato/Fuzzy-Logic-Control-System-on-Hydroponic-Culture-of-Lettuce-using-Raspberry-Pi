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

file = open("EC.txt", 'w')

input(print("Please dip on 12.88 ms/cm buffer solution and press Enter when ready."))

buf = list()
for i in range(60):
	ads1115.set_addr_ADS1115(0x48)
	#Sets the gain and input voltage range.
	ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
	adc1 = ads1115.read_voltage(1)
	rawEC = adc1['r']
	buf.append(rawEC)
	print("Getting Sensor Readings...")
	time.sleep(1)

buf.sort()
buf = buf[10:50]
EC1 = sum(map(float, buf))/40

print(EC1)	
	
input(print("Please dip on 1.413 ms/cm buffer solution and press Enter when ready."))

bak = list()
for i in range(60):
	ads1115.set_addr_ADS1115(0x48)
	#Sets the gain and input voltage range.
	ads1115.set_gain(ADS1115_REG_CONFIG_PGA_6_144V)
	adc1 = ads1115.read_voltage(1)
	rawEC = adc1['r']
	bak.append(rawEC)
	print("Getting Sensor Readings...")
	time.sleep(1)

bak.sort()
bak = bak[10:50]
EC2 = sum(map(float, bak))/40

x = float(EC1) - float(EC2)
m = 11.467 / x
y = m * float(EC1)
b = 12.88 - y
file.write("m="+str(m)+"\n")
file.write("b="+str(b)+"\n")
file.close()
input(print("Calibration Complete! press any key to exit."))
