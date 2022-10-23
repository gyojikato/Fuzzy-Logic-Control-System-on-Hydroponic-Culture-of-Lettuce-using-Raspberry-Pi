import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import DHT
import PH
import EC
import time
import RPi.GPIO as GPIO


in1 = 15
in2 = 18
in3 = 23
in4 = 24
in5 = 7
in6 = 12
in7 = 16
in8 = 20
Aena = 14
Aenb = 25
Bena = 8
Benb = 21


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(in5, GPIO.OUT)
GPIO.setup(in6, GPIO.OUT)
GPIO.setup(in7, GPIO.OUT)
GPIO.setup(in8, GPIO.OUT)
GPIO.setup(Aena, GPIO.OUT)
GPIO.setup(Aenb, GPIO.OUT)
GPIO.setup(Bena, GPIO.OUT)
GPIO.setup(Benb, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
GPIO.output(in5, GPIO.LOW)
GPIO.output(in6, GPIO.LOW)
GPIO.output(in7, GPIO.LOW)
GPIO.output(in8, GPIO.LOW)
p = GPIO.PWM(Aena, 16000)
p1 = GPIO.PWM(Aenb, 16000)
p2 = GPIO.PWM(Bena, 16000)
p3 = GPIO.PWM(Benb, 16000)
p.start(100)
p1.start(100)	
p2.start(100)
p3.start(100)


x = 0
temperature = ctrl.Antecedent(np.arange(15, 40, 1), 'temperature')
humidity = ctrl.Antecedent(np.arange(10, 100, 1), 'humidity')
Electric_Conductivity = ctrl.Antecedent(np.arange(0, 1.8, .1), 'Electric_Conductivity')
pH_Level = ctrl.Antecedent(np.arange(0, 6, .1), 'pH_Level')
Water_Level = ctrl.Antecedent(np.arange(3, 6, .1), 'Water_Level')
pH_LevelB = ctrl.Antecedent(np.arange(5, 8, .1), 'pH_LevelB')
fan_speed = ctrl.Consequent(np.arange(0, 2500, 1), 'fan_speed')
EC_Pump_Duration = ctrl.Consequent(np.arange(-1, 8, .1), 'EC_Pump_Duration')
Acidic_Pump_Duration = ctrl.Consequent(np.arange(-1, 8, .1), 'Acidic_Pump_Duration')
Alkaline_Pump_Duration = ctrl.Consequent(np.arange(-1, 8, .1), 'Alkaline_Pump_Duration')

temperature['cold'] = fuzz.trimf(temperature.universe, [15, 15, 20])
temperature['normal'] = fuzz.trimf(temperature.universe, [17, 25, 30])
temperature['hot'] = fuzz.trimf(temperature.universe, [27, 40, 40])
# temperature membership functions

humidity['dry'] = fuzz.trimf(humidity.universe, [1, 10, 45])
humidity['optimal'] = fuzz.trimf(humidity.universe, [35, 50, 70])
humidity['wet'] = fuzz.trimf(humidity.universe, [60, 100, 100])
# humidity membership functions

Electric_Conductivity['Very Low'] = fuzz.trimf(Electric_Conductivity.universe, [0, 0, 0.4])
Electric_Conductivity['Low'] = fuzz.trimf(Electric_Conductivity.universe, [0.2, 0.6, 0.8])
Electric_Conductivity['Medium'] = fuzz.trimf(Electric_Conductivity.universe, [0.6, 1, 1.2])
Electric_Conductivity['Normal'] = fuzz.trimf(Electric_Conductivity.universe, [1, 1.8, 1.8])
# electric conductivity membership functions

pH_Level['Very Low'] = fuzz.trimf(pH_Level.universe, [0, 0, 4.5])
pH_Level['Low'] = fuzz.trimf(pH_Level.universe, [4, 4.5, 5.5])
pH_Level['Normal'] = fuzz.trimf(pH_Level.universe, [5, 6, 6])

pH_LevelB['Normal'] = fuzz.trimf(pH_LevelB.universe, [5, 5, 6])
pH_LevelB['High'] = fuzz.trimf(pH_LevelB.universe, [5.5, 6.5, 7.5])
pH_LevelB['Very High'] = fuzz.trimf(pH_LevelB.universe, [7, 8, 8])
# ph level membership functions

Water_Level['Low'] = fuzz.trimf(Water_Level.universe, [3, 3, 4])
Water_Level['Medium'] = fuzz.trimf(Water_Level.universe, [3.5, 4.5, 5.5])
Water_Level['High'] = fuzz.trimf(Water_Level.universe, [5, 6, 6])
# water level membership functions

fan_speed['slow'] = fuzz.trimf(fan_speed.universe, [0, 0, 1000])
fan_speed['medium'] = fuzz.trimf(fan_speed.universe, [250, 1250, 2250])
fan_speed['fast'] = fuzz.trimf(fan_speed.universe, [1500, 2500, 2500])
# fan speed membership functions

EC_Pump_Duration['stop'] = fuzz.trimf(EC_Pump_Duration.universe, [-1, -1, 0])
EC_Pump_Duration['short'] = fuzz.trimf(EC_Pump_Duration.universe, [0, 1.5, 3])
EC_Pump_Duration['medium'] = fuzz.trimf(EC_Pump_Duration.universe, [3, 4, 5])
EC_Pump_Duration['long'] = fuzz.trimf(EC_Pump_Duration.universe, [5, 8, 8])
# ec pump membership functions

Acidic_Pump_Duration['stop'] = fuzz.trimf(Acidic_Pump_Duration.universe, [-1, -1, 0])
Acidic_Pump_Duration['short'] = fuzz.trimf(Acidic_Pump_Duration.universe, [0, 1.5, 3])
Acidic_Pump_Duration['medium'] = fuzz.trimf(Acidic_Pump_Duration.universe, [3, 4, 5])
Acidic_Pump_Duration['long'] = fuzz.trimf(Acidic_Pump_Duration.universe, [5, 8, 8])
# ph Up pump membership functions

Alkaline_Pump_Duration['stop'] = fuzz.trimf(Alkaline_Pump_Duration.universe, [-1, -1, 0])
Alkaline_Pump_Duration['short'] = fuzz.trimf(Alkaline_Pump_Duration.universe, [0, 1.5, 3])
Alkaline_Pump_Duration['medium'] = fuzz.trimf(Alkaline_Pump_Duration.universe, [3, 4, 5])
Alkaline_Pump_Duration['long'] = fuzz.trimf(Alkaline_Pump_Duration.universe, [5, 8, 8])
# ph down membership functions

def get_fan_speed_control_rules():
    rule1 = ctrl.Rule(
        temperature['cold'] & humidity['dry'],
        fan_speed['medium']
    )
    rule2 = ctrl.Rule(
        temperature['cold'] & humidity['optimal'],
        fan_speed['slow']
    )
    rule3 = ctrl.Rule(
        temperature['cold'] & humidity['wet'],
        fan_speed['slow']
    )
    rule4 = ctrl.Rule(
        temperature['normal'] & humidity['dry'],
        fan_speed['fast']
    )
    rule5 = ctrl.Rule(
        temperature['normal'] & humidity['optimal'],
        fan_speed['medium']
    )
    rule6 = ctrl.Rule(
        temperature['normal'] & humidity['wet'],
        fan_speed['slow']
    )
    rule7 = ctrl.Rule(
        temperature['hot'] & humidity['dry'],
        fan_speed['fast']
    )
    rule8 = ctrl.Rule(
        temperature['hot'] & humidity['optimal'],
        fan_speed['fast']
    )
    rule9 = ctrl.Rule(
        temperature['hot'] & humidity['wet'],
        fan_speed['fast']
    )

    return [
        rule1, rule2, rule3, rule4,
        rule5, rule6, rule7, rule8,
        rule9,
    ]


Temp_ctrl = ctrl.ControlSystem(
    get_fan_speed_control_rules()
)


def get_ec_pump_duration_control_rules():
    rule1 = ctrl.Rule(
        Electric_Conductivity['Very Low'] & Water_Level['Low'],
        EC_Pump_Duration['long']
    )
    rule2 = ctrl.Rule(
        Electric_Conductivity['Very Low'] & Water_Level['Medium'],
        EC_Pump_Duration['medium']
    )
    rule3 = ctrl.Rule(
        Electric_Conductivity['Very Low'] & Water_Level['High'],
        EC_Pump_Duration['medium']
    )
    rule4 = ctrl.Rule(
        Electric_Conductivity['Low'] & Water_Level['Low'],
        EC_Pump_Duration['long']
    )
    rule5 = ctrl.Rule(
        Electric_Conductivity['Low'] & Water_Level['Medium'],
        EC_Pump_Duration['medium']
    )
    rule6 = ctrl.Rule(
        Electric_Conductivity['Low'] & Water_Level['High'],
        EC_Pump_Duration['medium']
    )
    rule7 = ctrl.Rule(
        Electric_Conductivity['Medium'] & Water_Level['Low'],
        EC_Pump_Duration['short']
    )
    rule8 = ctrl.Rule(
        Electric_Conductivity['Medium'] & Water_Level['Medium'],
        EC_Pump_Duration['short']
    )

    rule9 = ctrl.Rule(
        Electric_Conductivity['Medium'] & Water_Level['High'],
        EC_Pump_Duration['short']
    )
    rule10 = ctrl.Rule(
        Electric_Conductivity['Normal'] & Water_Level['Low'],
        EC_Pump_Duration['stop']
    )
    rule11 = ctrl.Rule(
        Electric_Conductivity['Normal'] & Water_Level['Medium'],
        EC_Pump_Duration['stop']
    )
    rule12 = ctrl.Rule(
        Electric_Conductivity['Normal'] & Water_Level['High'],
        EC_Pump_Duration['stop']
    )

    return [
        rule1, rule2, rule3, rule4,
        rule5, rule6, rule7, rule8,
        rule9, rule10, rule11, rule12,
    ]


EC_ctrl = ctrl.ControlSystem(
    get_ec_pump_duration_control_rules()
)


def get_acidic_pump_duration():
    rule1 = ctrl.Rule(
        pH_Level['Very Low'] & Water_Level['Low'],
        Acidic_Pump_Duration['long']
    )

    rule2 = ctrl.Rule(
        pH_Level['Very Low'] & Water_Level['Medium'],
        Acidic_Pump_Duration['long']
    )

    rule3 = ctrl.Rule(
        pH_Level['Very Low'] & Water_Level['High'],
        Acidic_Pump_Duration['medium']
    )

    rule4 = ctrl.Rule(
        pH_Level['Low'] & Water_Level['Low'],
        Acidic_Pump_Duration['long']
    )

    rule5 = ctrl.Rule(
        pH_Level['Low'] & Water_Level['Medium'],
        Acidic_Pump_Duration['medium']
    )

    rule6 = ctrl.Rule(
        pH_Level['Low'] & Water_Level['High'],
        Acidic_Pump_Duration['short']
    )
    rule7 = ctrl.Rule(
        pH_Level['Normal'] & Water_Level['Low'],
        Acidic_Pump_Duration['stop']
    )

    rule8 = ctrl.Rule(
        pH_Level['Normal'] & Water_Level['Medium'],
        Acidic_Pump_Duration['stop']
    )

    rule9 = ctrl.Rule(
        pH_Level['Normal'] & Water_Level['High'],
        Acidic_Pump_Duration['stop']
    )

    return [
        rule1, rule2, rule3,
        rule4, rule5, rule6,
        rule7, rule8, rule9,
    ]


Acidic_ctrl = ctrl.ControlSystem(
    get_acidic_pump_duration()
)


def get_alkaline_pump_duration():
    rule1 = ctrl.Rule(
        pH_LevelB['Very High'] & Water_Level['Low'],
        Alkaline_Pump_Duration['long']
    )

    rule2 = ctrl.Rule(
        pH_LevelB['Very High'] & Water_Level['Medium'],
        Alkaline_Pump_Duration['medium']
    )

    rule3 = ctrl.Rule(
        pH_LevelB['Very High'] & Water_Level['High'],
        Alkaline_Pump_Duration['medium']
    )

    rule4 = ctrl.Rule(
        pH_LevelB['High'] & Water_Level['Low'],
        Alkaline_Pump_Duration['medium']
    )

    rule5 = ctrl.Rule(
        pH_LevelB['High'] & Water_Level['Medium'],
        Alkaline_Pump_Duration['medium']
    )

    rule6 = ctrl.Rule(
        pH_LevelB['High'] & Water_Level['High'],
        Alkaline_Pump_Duration['short']
    )
    rule7 = ctrl.Rule(
        pH_LevelB['Normal'] & Water_Level['Low'],
        Alkaline_Pump_Duration['stop']
    )

    rule8 = ctrl.Rule(
        pH_LevelB['Normal'] & Water_Level['Medium'],
        Alkaline_Pump_Duration['stop']
    )

    rule9 = ctrl.Rule(
        pH_LevelB['Normal'] & Water_Level['High'],
        Alkaline_Pump_Duration['stop']
    )

    return [
        rule1, rule2, rule3,
        rule4, rule5, rule6,
        rule7, rule8, rule9,
    ]


Alkaline_ctrl = ctrl.ControlSystem(
    get_alkaline_pump_duration()
)


file = open(time.strftime('Sensor_Reading_%m_%d_%Y_%H_%M_%S.txt'), 'w')
file.write('date and time, Temperature C, Humidity %, EC Level ms/c, pH Level \n')

try:
	while True:
		# Prints into a CSV file
		file.write(time.strftime('%m/%d/%Y %H:%M:%S') + (', ') +str(round(DHT.getTemp() ,2)) + ', ' +str(round(DHT.getHum() ,2)) + ', '
		+ str(round(EC.getEC() ,2)) + ', ' + str(round(PH.getPH() ,2)) + '\n')
		# Prints to Console           
		print('EC Level: ' +str(EC.getEC()) + 'ms/cm')
		print('PH Level: ' +str(PH.getPH()))
		print('Temperature: ' +str(DHT.getTemp()) + 'C')
		print('Humidity: ' +str(DHT.getHum()) + '%')
		
		speed = ctrl.ControlSystemSimulation(Temp_ctrl)
		speed.input['temperature'] = DHT.getTemp()
		speed.input['humidity'] = DHT.getHum()
		speed.compute()
		
		duration = ctrl.ControlSystemSimulation(EC_ctrl)
		duration.input['Electric_Conductivity'] = EC.getEC()
		duration.input['Water_Level'] = EC.getWL()
		duration.compute()
		acduration = ctrl.ControlSystemSimulation(Acidic_ctrl)
		acduration.input['pH_Level'] = PH.getPH()
		acduration.input['Water_Level'] = EC.getWL()
		acduration.compute()
		akduration = ctrl.ControlSystemSimulation(Alkaline_ctrl)
		akduration.input['pH_LevelB'] = PH.getPH()
		akduration.input['Water_Level'] = EC.getWL()
		akduration.compute()
		#fan
		GPIO.output(in7, GPIO.HIGH)
		GPIO.output(in8, GPIO.LOW)
		dc = speed.output['fan_speed'] / 24
		p3.ChangeDutyCycle(dc)
		time.sleep(1);
		# EC pump
		p.start(100)
		GPIO.output(in1, GPIO.LOW)
		GPIO.output(in2, GPIO.HIGH)
		if duration.output['EC_Pump_Duration'] < 0:
			duration.output['EC_Pump_Duration'] = 0
		time.sleep(duration.output['EC_Pump_Duration']);
		GPIO.output(in1, GPIO.LOW)
		GPIO.output(in2, GPIO.LOW)
		# PH Up pump
		p1.start(100)
		GPIO.output(in3, GPIO.LOW)
		GPIO.output(in4, GPIO.HIGH)
		if acduration.output['Acidic_Pump_Duration'] < 0:
			acduration.output['Acidic_Pump_Duration'] = 0
		time.sleep(acduration.output['Acidic_Pump_Duration'])
		GPIO.output(in3, GPIO.LOW)
		GPIO.output(in4, GPIO.LOW)
		# PH Down pump
		p2.start(100)
		GPIO.output(in5, GPIO.LOW)
		GPIO.output(in6, GPIO.HIGH)
		if akduration.output['Alkaline_Pump_Duration'] < 0:
			akduration.output['Alkaline_Pump_Duration'] = 0
		time.sleep(akduration.output['Alkaline_Pump_Duration'])
		GPIO.output(in5, GPIO.LOW)
		GPIO.output(in6, GPIO.LOW)
        # 10 mins delay (while still printing values to console and csv) to let the solution adjust         
	
		while x < 150:
			print('EC Level: '+str(EC.getEC())+'ms/cm')
			print('PH Level: '+str(PH.getPH()))
			print('Temperature: '+str(DHT.getTemp())+'C')
			print('Humidity: '+str(DHT.getHum())+'%')
			file.write(time.strftime('%m/%d/%Y %H:%M:%S')+(', ')+str(round(DHT.getTemp() ,2))+', '+str(round(DHT.getHum() ,2))+', '+str(round(EC.getEC() ,2))+', '+str(round(PH.getPH() ,2))+'\n')
			time.sleep(2);
			x += 1
		x = 0
	
except KeyboardInterrupt:
	running = False
	file.close()
