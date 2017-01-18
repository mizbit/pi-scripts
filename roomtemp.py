# *-* coding: utf-8 -*-
import re
import requests
import Adafruit_DHT
import math
execfile('/home/pi/.wu_config.py')
from urllib import urlencode
import urllib2

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 18
WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

def c_to_f(input_temp):
    # convert input_temp from Celsius to Fahrenheit
    return (input_temp * 1.8) + 32

def dew_point(celsius, humidity):
    a = 17.271
    b = 237.7
    temp = (a * celsius) / (b + celsius) + math.log(humidity*0.01)
    dew = (b * temp) / (a - temp)
    return dew

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

with open('/sys/bus/w1/devices/28-031663113dff/w1_slave', 'r') as temp_file:
    for line in temp_file:
        line = re.findall(r't=.*', line)
        if line:
            line = line[0].split('=')[1]
            ds_temp0 = int(line)

ds_temp1 = ds_temp0 / 1000
ds_temp2 = ds_temp0 / 100
ds_tempM = ds_temp2 % ds_temp1
ds_temp = str(ds_temp1) + '.' + str(ds_tempM)
print('DS Temperature: %s°C' % str(ds_temp))

dht_humidity, dht_temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if dht_humidity is not None and dht_temp is not None:
    print('DHT Temperature: {0:0.1f}°C DHT Humidity: {1:0.1f}%'.format(dht_temp, dht_humidity))
    dewpoint = dew_point(int(float(ds_temp)), dht_humidity)
    print('Dew Point: %s°C' % str(round(dewpoint, 2)))

	# Post to Weather Underground PWS (Personal Weather Station)
    print('Uploading data to Weather Underground...')
    weather_data = {
        'action': 'updateraw',
        'ID': Config.STATION_ID,
        'PASSWORD': Config.STATION_KEY,
        'dateutc': 'now',
        'tempf': str(c_to_f(int(float(ds_temp)))),
        'humidity': str(dht_humidity),
        'dewptf': str(c_to_f(dewpoint)),
    }
    upload_url = WU_URL + '?' + urlencode(weather_data)
    response = urllib2.urlopen(upload_url)
    html = response.read()
    print('Server response: ' + html)
    response.close()

	# Post to Google Spreadsheet via IFTTT
    print('Triggerring IFTTT event...')
    maker_url = 'https://maker.ifttt.com/trigger/roomtemp/with/key/' + maker_key + '?value1=' + ds_temp + '&value2=' + str(dht_humidity) + '&value3=' + str(round(dewpoint, 2))
    content = requests.get(maker_url).text
    print(content)
else:
    dht_temp = 0
    dht_humidity = 0
    print('Failed to get DHT reading. Try again!')
