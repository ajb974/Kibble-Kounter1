from time import sleep
from picamera import PiCamera

def info():  
    '''Prints a basic library description'''
    print("Software library for the KibbleKounter project.")

def setupCamera():
    camera = PiCamera()
    camera.resolution = (2592, 1944)
    camera.framerate = 15

def takePicture():
    camera.start_preview()
    sleep(5)
    campera.capture('/home/pi/Desktop/piimage.jpg')
    camera.stop_preview()
    print("A picture was taken.")
