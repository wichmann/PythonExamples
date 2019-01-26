#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wetterstation mit der SenseHat-Erweiterung.

@author: Christian Wichmann
@license: GNU GPL
"""

import time
import json
import requests
from datetime import datetime

from sense_hat import SenseHat


# setze alle notwendigen Konstanten
TIMEOUT_DISPLAY = 5
SPEED = 0.07
WEATHER_MAPPING = {
    'Mist': 'Nebel',
    'Rain': 'Regen',
    'Drizzle': 'Nieselregen',
    'Thunderstorm': 'Sturm',
    'Snow': 'Schnee',
    'Clear': 'Klar',
    'Clouds': 'Wolken'
}
TEMP_COLOR = [0,0,255]
HUMIDITY_COLOR = [0,255,0]


# initialisiere SenseHat-Erweiterung
sense = SenseHat()
sense.low_light = True


def get_location():
    """Ermittelt die Stadt zur eigenen IP-Adresse."""
    url = "https://ipinfo.io/"
    try:
        r = requests.get(url)
    except:
        print("error while querying info...")
    data = json.loads(r.text)
    return data['city']


def get_weather(city):
    """Fragt das aktuelle Wetter bei openweathermap.org ab und gibt Temperatur,
    Luftfeuchtigkeit, Windgeschwindigkeit und die Zeiten von Sonnenaufgang und
    Sonnenuntergang zurück."""
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'
    app_id = '' # <- insert API key for openweathermap.org
    r = requests.get(url.format(city, app_id))
    data = json.loads(r.text)
    weather = data['weather'][0]['main']
    temp = data['main']['temp'] - 273.15
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(data['sys']['sunset'])
    return weather, temp, humidity, wind_speed, sunrise, sunset


def show_weather_info():
    """Gibt die aktuellen Wetterwerte über die SenseHat-Erweiterung aus."""
    # hole Wetter für aktuellen Standort
    weather, temp, humidity, wind_speed, sunrise, sunset = get_weather(get_location())
    # lese Werte aus SenseHat-Erweiterung aus
    temp_interior = sense.get_temperature() # sense.get_temperature_from_humidity()
    temp_interior_alt = sense.get_temperature_from_pressure()
    pressure_interior = sense.get_pressure()
    humidity_interior = sense.get_humidity()
    # gib aktuelle Werte aus
    sense.show_message("Innentemperatur: {:.1f}".format(temp_interior),
                       scroll_speed=SPEED, text_colour=TEMP_COLOR)
    sense.show_message("Luftfeuchte (innen): {:.1f} %".format(humidity_interior),
                       scroll_speed=SPEED, text_colour=HUMIDITY_COLOR)
    sense.show_message("Aussentemperatur: {:.1f}".format(temp),
                       scroll_speed=SPEED, text_colour=TEMP_COLOR)
    sense.show_message("Luftfeuchte (aussen): {:.1f} %".format(humidity),
                       scroll_speed=SPEED, text_colour=HUMIDITY_COLOR)
    sense.show_message("Wetter: {}".format(WEATHER_MAPPING[weather]),
                       scroll_speed=SPEED)
    sense.show_message("Windgeschwindigkeit: {} m/s".format(wind_speed),
                       scroll_speed=SPEED)
    sense.show_message("Sonnenaufgang: {}".format(sunrise.strftime('%H:%M:%S')),
                       scroll_speed=SPEED)
    sense.show_message("Sonnenuntergang: {}".format(sunset.strftime('%H:%M:%S')),
                       scroll_speed=SPEED)


if __name__ == '__main__':
    try:
        while True: 
            show_weather_info()
            # überprüfe, ob das Steuerkreuz nach unten gedrückt wurde
            for event in sense.stick.get_events():
                if 'down' in event.direction:
                    exit()
            time.sleep(TIMEOUT_DISPLAY)
    except KeyboardInterrupt:
        sense.clear()
        print('Tschüß!')
