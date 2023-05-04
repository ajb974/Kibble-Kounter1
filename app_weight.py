import KibbleKounter as kk
from threading import Thread, Lock, Event
from queue import Queue
import time
from datetime import datetime
import csv
#from teachablemachinepython import tmlib
#from  tmblib import *
#import cv2
import numpy as np
import os
#from random import randint

TOL_WATER=0
TOL_FOOD=0 #tolerance for food and water to trigger change
FOLDER_NAME="pets"
DATA_FILE="pet_data.csv"
empty_water_bowl=None
#curr_water_bowl=None
full_water_bowl=None
#curr_food_bowl=None
full_food_bowl=None

queue_water=Queue()
lock_water=Lock()
queue_weight=Queue()
lock_weight=Lock()

#camera = kk.setupCamera()
file_number = 0

#tm = TeachableMachineTF()
#tm.load('/home/pi/Kibble-Kounter1/teachablemachinepython/tflite_model/model_unquant.tfile','/home/pi/Kibble-Kounter1/teachablemachinepython/tflite_model/labels.txt')

#function for making folders to store pictures in (e.g. for camera_training)
def make_folder(folder_name):
   os.mkdir('/home/pi/Desktop/pictures/%s' % folder_name)


def first_setup(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["water_percent", "weight_percent", "time","pet"]
        #field = ["water_precent", "weight_precent", "predicted_name", "predicted_idx", "time"]
        writer.writerow(field)

def camera_training(folder_name, done):
    global file_number
    if done == False:
      file_name = "pictures/"+folder_name+"/"+folder_name+str(file_number)
      kk.takePicture(camera, file_name)
      file_number+=1
    else:
      file_number=0


def zero_sensors():
    global empty_water_bowl
    kk.setupProximitySensor()
    kk.zeroScale()
    empty_water_bowl=kk.measureDistance()

def test_sensors():
    global full_water_bowl, full_food_bowl
    kk.TestScale()
    full_water_bowl=kk.measureDistance()
    full_food_bowl=kk.readScale_grams()

def read_weight():
    while True:
        with lock_weight:
            queue_weight.put(kk.readScale_grams())
        time.sleep(1)

def read_water():
    while True:
        with lock_water:
            queue_water.put(kk.measureDistance())
        time.sleep(1)



def save_reading(pet_name):
    curr_water_bowl=full_water_bowl
    curr_food_bowl=full_food_bowl
    test_water=None
    test_food=None
    is_eating=False
    def test_reading():
        if ((curr_water_bowl-TOL_WATER) <= test_water <= (curr_water_bowl+TOL_WATER)):
            if ((curr_food_bowl-TOL_FOOD) <= test_food <= (curr_food_bowl+TOL_FOOD)):
                return False
        return True

    while True:
        test_water=queue_water.get()
        test_food=queue_weight.get()
        if (test_reading()):
            #event_camera.set()
            is_eating=True
            curr_water_bowl=test_water
            curr_food_bowl=test_food
        else:
            if is_eating:
                print("save1")
                is_eating=False
                now=datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                curr_water_percent=(full_water_bowl/curr_water_bowl)*100
                curr_food_percent=(full_food_bowl/curr_food_bowl)*100
                #curr_prediction = camera_prediction()
                pet_file=pet_name+".csv"
                with open(pet_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([str(curr_water_percent), str(curr_food_percent), dt_string, pet_name])
                    #writer.writerow([str(cur_water_present), str(curr_food_present), curr_prediction[0], curr_prediction[1], dt_string])
                    print("save2")


def save_reading1(pet_name):
    curr_water_bowl=full_water_bowl
    curr_food_bowl=full_food_bowl
    test_water=None
    test_food=None
    is_eating=False
    def test_reading():
        if ((curr_water_bowl-TOL_WATER) <= test_water <= (curr_water_bowl+TOL_WATER)):
            if ((curr_food_bowl-TOL_FOOD) <= test_food <= (curr_food_bowl+TOL_FOOD)):
                return False
        return True
    
    while True:
        test_water=queue_water.get()
        test_food=queue_weight.get()
        is_eating=test_reading()
        if is_eating==True:
            curr_water_bowl=test_water
            curr_food_bowl=test_food
            
            
            is_eating=False
            now=datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            curr_water_percent=round(((full_water_bowl/curr_water_bowl)*100),2)
            curr_food_percent=round(((full_food_bowl/curr_food_bowl)*100),2)
            if curr_water_percent<0:
                curr_water_percent=0
            if curr_food_percent<0:
                curr_food_percent=0
            #curr_prediction = camera_prediction()
            pet_file=pet_name+".csv"
            with open(pet_file, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(curr_water_percent), str(curr_food_percent), dt_string, pet_name])
                #writer.writerow([str(cur_water_present), str(curr_food_present), curr_prediction[0], curr_prediction[1], dt_string])


'''
def camera_prediction():
     cap = cv2.VideoCapture(0)
     _, img = cap.read()
     res,name = tm.predict(img)
     idx = np.argmax(res)
     s = [name, str(idx)]
     return s
'''

def start_device(pet_name):
    weight_thread=Thread(target=read_weight)
    water_thread=Thread(target=read_water)
    reading_thread=Thread(target=save_reading1,args=[pet_name])
    weight_thread.start()
    water_thread.start()
    reading_thread.start()

