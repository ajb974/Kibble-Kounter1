from time import sleep
from picamera import PiCamera
from hx711 import HX711		# import the class HX711
import RPi.GPIO as GPIO		# import GPIO
import time
import statistics

camera = None
DataPin = 23
ClockPin = 24
NumReadings = 10
hx = None
ZeroValue=None
TestValue=None #difference in scale value after weight is put on
TestWeight=100 #grams


GPIO_TRIGGER = 17
GPIO_ECHO = 18


def info():  
    '''Prints a basic library description'''
    print("Software library for the KibbleKounter project.")

def setupProximitySensor():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
  GPIO.setup(GPIO_ECHO, GPIO.IN)
  return True

def measureDistance():
  #set trigger to HIGH
  GPIO.setmode(GPIO.BCM)
  setupProximitySensor()
  GPIO.output(GPIO_TRIGGER, True)

  #set trigger after 0.01 ms to LOW
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)

 
  StartTime = time.time()
  StopTime = time.time()
  CurrTime = StartTime

  while time.time()-CurrTime<10:
  #save StartTime
    if GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    if GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

  #time difference between start and arrival
  TimeElapsed = StopTime - StartTime
  distance = (TimeElapsed * 34300) / 2 #in cm
  if time.time()-CurrTime>10:
      return -1
  return distance

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
    if result:			# check if the reset was successful
        print('Ready to use')
    else:
        print('not ready')
def readScale_raw():
    #resetScale()
    data = hx.get_raw_data(NumReadings)
    return data #returns list of readings
def zeroScale():
    global hx,ZeroValue
    hx=HX711(dout_pin=DataPin, pd_sck_pin=ClockPin, gain=64, channel='A')
    resetScale()
    data = readScale_raw()
    ZeroValue=statistics.median(data) #take median of list of readings
def TestScale():
    global TestValue
    data=readScale_raw()
    TestValue=statistics.median(data)-ZeroValue #differnce between scale with weight and zero
def readScale_grams():
    data=readScale_raw()
    ScaleValue=statistics.median(data) #raw scale value
    ScaleDiff=ScaleValue-ZeroValue #difference between zero and current
    ScaleGrams=(ScaleDiff/TestValue)*TestWeight #convert to grams
    print("ScaleDiff "+str(ScaleDiff))
    return ScaleGrams
