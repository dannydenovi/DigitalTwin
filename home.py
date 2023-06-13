import RPi.GPIO as GPIO
import Adafruit_DHT
import argparse
import signal
import sys
from threading import Thread
from random import randint
from paho.mqtt.client import Client as mqtt
from time import sleep

parser = argparse.ArgumentParser(description='Argument parsing')
parser.add_argument('-r', '--random', action='store_true', help='Generate random values for temperature.')
args = parser.parse_args()


Broker=mqtt(client_id="raspberry")
Broker.connect("localhost", 1883)

DOOR_LED = 19
DOOR_PIN = 18

LIGHT_LED = 26
LIGHT_PIN = 23

HOT_AIR_PIN = 24
COLD_AIR_PIN = 25


GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_LED, GPIO.OUT)
GPIO.setup(DOOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(LIGHT_LED, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(HOT_AIR_PIN, GPIO.OUT)
GPIO.setup(COLD_AIR_PIN, GPIO.OUT)

door_state = False  
light_state = False

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

# Imposta il gestore del segnale di interruzione
signal.signal(signal.SIGINT, signal_handler)

def manage_temp(temperature):
    if temperature < 13:
        msg = "hot_air"
        GPIO.output(HOT_AIR_PIN, GPIO.HIGH)
        GPIO.output(COLD_AIR_PIN, GPIO.LOW)

    elif temperature > 23:
        msg = "cold_air"
        GPIO.output(HOT_AIR_PIN, GPIO.LOW)
        GPIO.output(COLD_AIR_PIN, GPIO.HIGH)
    else:
        msg = "off"
        GPIO.output(HOT_AIR_PIN, GPIO.LOW)
        GPIO.output(COLD_AIR_PIN, GPIO.LOW)

    return msg

def measure_temp():
    while True:
        if not args.random:
            try:
                _, temperature = Adafruit_DHT.read_retry(11, 4)
                msg = manage_temp(temperature)
            except:
                msg = "off"
        else:
            msg = manage_temp(randint(0, 40))
        
        Broker.publish(topic="air_conditioner", payload=str(msg))
        sleep(2)


def door_button_callback(channel):
    global door_state
    
    if door_state:
        msg = "close"
        GPIO.output(DOOR_LED, GPIO.LOW)
        door_state = False

    else:
        msg = "open"
        GPIO.output(DOOR_LED, GPIO.HIGH)
        door_state = True
    
    Broker.publish(topic="door", payload=str(msg))


def light_button_callback(channel):
    global door_state
    
    if door_state:
        msg = "off"
        GPIO.output(LIGHT_LED, GPIO.LOW)
        door_state = False
    else:
        msg = "on"
        GPIO.output(LIGHT_LED, GPIO.HIGH)
        door_state = True
    
    Broker.publish(topic="main_light", payload=str(msg))

GPIO.add_event_detect(DOOR_PIN, GPIO.FALLING, callback=door_button_callback, bouncetime=200)
GPIO.add_event_detect(LIGHT_PIN, GPIO.FALLING, callback=light_button_callback, bouncetime=200)

temp_thread = Thread(target=measure_temp)
temp_thread.start()

try:
    while True:
        pass

finally:
    GPIO.cleanup()

