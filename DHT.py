import time
import board
import adafruit_dht
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)


def getTemp():
    try:
        temp = dhtDevice.temperature
        return checkVal(temp)
    except:
        
        return getTemp()

def getHum():
    try:
        hum = dhtDevice.humidity
        return checkVal(hum)
    except:
        
        return getHum()

def checkVal(value):
    
    try:
        return float(value)
    except:
        return 0
   

