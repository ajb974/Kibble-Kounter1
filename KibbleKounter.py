from time import sleep
from picamera import PiCamera

camera = PiCamera()

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
