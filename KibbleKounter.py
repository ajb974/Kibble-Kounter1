from time import sleep
from picamera import PiCamera
from hx711 import HX711		# import the class HX711
import RPi.GPIO as GPIO		# import GPIO
import time

camera = PiCamera()

DataPin = 23
ClockPin = 24
NumReadings = 10
hx = HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=128, channel='A')
def info():  
    '''Prints a basic library description'''
    print("Software library for the KibbleKounter project.")

def setupCamera():
    #Sets up Camera
    #Sets resolutions of camera to highest resolution
    camera.resolution = (2592, 1944)
    #Sets framerate to support highest resolution
    camera.framerate = 15

def takePicture():
    #takes a still (image) using camera
    #starts live display of cameras input
    camera.start_preview()
    #delay of 5 seconds
    sleep(5)
    #captures the still and saves it to desktop
    campera.capture('/home/pi/Desktop/piimage.jpg')
    #stops camera input
    camera.stop_preview()
    print("A picture was taken.")
def resetScale():
    result = hx.reset()	
def readScale():
    resetScale()
    data = hx.get_raw_data(NumReadings)
    return data #returns list of readings

