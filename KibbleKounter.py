from time import sleep
from picamera import PiCamera
from hx711 import HX711		# import the class HX711
import RPi.GPIO as GPIO		# import GPIO
import time

camera = None

DataPin = 23
ClockPin = 24
NumReadings = 10
hx = HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=128, channel='A')
def info():  
    '''Prints a basic library description'''
    print("Software library for the KibbleKounter project.")

def setupCamera():
    #Sets up Camera
    camera = PiCamera()
    #Sets resolutions of camera to highest resolution
    camera.resolution = (2592, 1944)
    #Sets framerate to support highest resolution
    camera.framerate = 15
    return camera

def takePicture(camera, filename):
    #takes a still (image) using camera
    #starts live display of cameras input
    camera.start_preview()
    #captures the still and saves it to desktop
    camera.capture('/home/pi/Desktop/%s.jpg' % filename)
    #stops camera input
    camera.stop_preview()
    return ('/home/pi/Desktop/%s.jpg' % filename) 

def resetScale():
    result = hx.reset()	
def readScale():
    resetScale()
    data = hx.get_raw_data(NumReadings)
    return data #returns list of readings

