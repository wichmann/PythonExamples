#!/usr/bin/env python3

import time
import json
import requests
from datetime import datetime

import paho.mqtt.client as mqtt
from sense_hat import SenseHat


BROKER_URL = '192.168.24.25'
CYCLE_TIME = 10


# initialisiere SenseHat-Erweiterung
sense = SenseHat()
sense.low_light = True


def get_location():
    """Ermittelt die Stadt zur eigenen IP-Adresse."""
    IP_LOCKUP_URL = "https://ipinfo.io/"
    try:
        r = requests.get(IP_LOCKUP_URL)
    except:
        print("error while querying info...")
    data = json.loads(r.text)
    return data['city']


def get_weather(city):
    """Fragt das aktuelle Wetter bei openweathermap.org ab und gibt Temperatur,
    Luftfeuchtigkeit, Windgeschwindigkeit und die Zeiten von Sonnenaufgang und
    Sonnenuntergang zurück."""
    URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'
    API_KEY = '' # <- insert API key for openweathermap.org
    r = requests.get(URL.format(city, API_KEY))
    data = json.loads(r.text)
    if data['cod'] == '404':
        return '', 0, 0, 0, '', ''
    weather = data['weather'][0]['main']
    temp = data['main']['temp'] - 273.15
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(data['sys']['sunset'])
    return weather, temp, humidity, wind_speed, sunrise, sunset


if __name__ == '__main__':
    try:
        mqttc = mqtt.Client()
        mqttc.connect(BROKER_URL, 1883, 60)
        while True:
            weather, temp, humidity, wind_speed, sunrise, sunset = get_weather(get_location())
            mqttc.publish('umgebung/wetter', str(weather))
            mqttc.publish('umgebung/temperatur', str(temp))
            mqttc.publish('umgebung/luftfeuchtigkeit', str(humidity))
            mqttc.publish('umgebung/windgeschwindigkeit', str(wind_speed))
            mqttc.publish('umgebung/sonnenaufgang', str(sunrise))
            mqttc.publish('umgebung/sonnenuntergang', str(sunset))
            mqttc.publish('wohnzimmer/temperatur', str(sense.get_temperature()))
            mqttc.publish('wohnzimmer/luftdruck', str(sense.get_pressure()))
            mqttc.publish('wohnzimmer/luftfeuchtigkeit', str(sense.get_humidity()))
            # überprüfe, ob das Steuerkreuz nach unten gedrückt wurde
            for event in sense.stick.get_events():
                if 'down' in event.direction:
                    exit()
            time.sleep(CYCLE_TIME)
    except KeyboardInterrupt:
        mqttc.disconnect()
        sense.clear()
        print('Tschüß!')
