#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Wetterserver mit Ausgabe auf der SenseHat-Erweiterung.

@author: Christian Wichmann
@license: GNU GPL
"""

import time
import json
import requests
import threading
from datetime import datetime

from flask import Flask
from flask import request
from sense_hat import SenseHat


# setze alle notwendigen Konstanten
TIMEOUT_DISPLAY = 5
TIMEOUT_UPDATE = 10
SPEED = 0.07
WEATHER_MAPPING = {
    '': '',
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
TIME_COLOR = [255,255,0]


# globale Variablen für die Kommunikation zwischen den Threads
weather = ''
temp = 0.0
humidity = 0.0
wind_speed = 0.0
sunrise = datetime.now()
sunset = datetime.now()
temp_interior = 0.0
temp_interior_alt = 0.0
pressure_interior = 0.0
humidity_interior = 0.0


# initialisiere Flask server
app = Flask(__name__)


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


def get_weather_for_city(city):
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


def update_weather_data():
    global weather, temp, humidity, wind_speed, sunrise, sunset, temp_interior, temp_interior_alt, pressure_interior, humidity_interior
    while True:
        print('Aktualisiere Wetter-Daten...')
        # hole Wetter für aktuellen Standort
        weather, temp, humidity, wind_speed, sunrise, sunset = get_weather_for_city(get_location())
        # lese Werte aus SenseHat-Erweiterung aus
        for i in range(10):
            print('Aktualisiere Sensor-Daten')
            temp_interior = sense.get_temperature() # sense.get_temperature_from_humidity()
            temp_interior_alt = sense.get_temperature_from_pressure()
            pressure_interior = sense.get_pressure()
            humidity_interior = sense.get_humidity()
            time.sleep(TIMEOUT_UPDATE)


def show_weather_info():
    global temp
    """Gibt die aktuellen Wetterwerte über die SenseHat-Erweiterung aus."""
    sense.show_message('Innentemperatur: {:.1f}'.format(temp_interior),
                       scroll_speed=SPEED, text_colour=TEMP_COLOR)
    sense.show_message('Luftfeuchte (innen): {:.1f} %'.format(humidity_interior),
                       scroll_speed=SPEED, text_colour=HUMIDITY_COLOR)
    sense.show_message('Aussentemperatur: {:.1f}'.format(temp),
                       scroll_speed=SPEED, text_colour=TEMP_COLOR)
    sense.show_message('Luftfeuchte (aussen): {:.1f} %'.format(humidity),
                       scroll_speed=SPEED, text_colour=HUMIDITY_COLOR)
    sense.show_message('Wetter: {}'.format(WEATHER_MAPPING[weather]),
                       scroll_speed=SPEED)
    sense.show_message('Windgeschwindigkeit: {} m/s'.format(wind_speed),
                       scroll_speed=SPEED)
    sense.show_message('Sonnenaufgang: {}'.format(sunrise.strftime('%H:%M:%S')),
                       scroll_speed=SPEED, text_colour=TIME_COLOR)
    sense.show_message('Sonnenuntergang: {}'.format(sunset.strftime('%H:%M:%S')),
                       scroll_speed=SPEED, text_colour=TIME_COLOR)


def update_display():
    time.sleep(TIMEOUT_DISPLAY)
    while True: 
        print('Starte Ausgabe auf Display...')
        show_weather_info()
        # überprüfe, ob das Steuerkreuz nach unten gedrückt wurde
        for event in sense.stick.get_events():
            if 'down' in event.direction:
                exit()
        time.sleep(TIMEOUT_DISPLAY)


@app.route('/')
def get_info():
    return 'Wetterstation Version 1.0'


@app.route('/temperature/interior')
def get_temp_interior():
    return '{}'.format(temp_interior)


@app.route('/temperature/exterior')
def get_temp():
    return '{}'.format(temp)


@app.route('/humidity/interior')
def get_humidity_interior():
    return '{}'.format(humidity_interior)


@app.route('/humidity/exterior')
def get_humidity():
    return '{}'.format(humidity)


@app.route('/weather')
def get_weather_status():
    return '{}'.format(weather)


@app.route('/wind/speed')
def get_wind_speed():
    return '{}'.format(wind_speed)


@app.route('/sun/sunrise')
def get_sunrise():
    return '{}'.format(sunrise)


@app.route('/sun/sunset')
def get_sunset():
    return '{}'.format(sunset)


if __name__ == '__main__':
    try:
        # starte Hintergrund-Thread für das Laden der Wetterdaten
        thread1 = threading.Thread(target=update_weather_data, args=())
        # setze das Daemon-Flag, damit der Thread beendet wird, wenn der
        # Web-Server durch Ctrl+C abgebrochen wird
        thread1.daemon = True
        thread1.start()
        # starte Hintergrund-Thread für das Display
        thread2 = threading.Thread(target=update_display, args=())
        thread2.daemon = True
        thread2.start()
        # starte Web-Server zur Steuerung des Lauflichts
        app.run(host= '0.0.0.0', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        sense.clear()
        print('Tschüß!')
