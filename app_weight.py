import KibbleKounter as kk
from threading import Thread, Lock, Event
from queue import Queue
import time
import datetime
import csv
from  tmblib import *
import numpy as np

TOL_WATER=5
TOL_FOOD=10 #tolerance for food and water to trigger change
DATA_FILE="data.csv"
PREDICTION_FILE="prediction.csv"
empty_water_bowl=None
#curr_water_bowl=None
full_water_bowl=None
#curr_food_bowl=None
full_food_bowl=None

queue_water=Queue()
queue_weight=Queue()

event_camera = Event()

camera = kk.setupCamera()
file_number = 0

tm = TeachableMachineTF()
tm.load('/home/pi/Kibble-Kounter1/teachablemachine-python/tflite_model/model_unquant.tfile','/home/pi/teachablemachine-python/tflite_model/labels.txt')


def first_setup():
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["water_percent", "weight_percent", "time"]
        writer.writerow(field)
    with open(PREDICTION_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["name", "id", "time"]
        writer.writerow(field)
def camera_training(folder_name, done):
    global file_number
    if not done:
      file_name = folder_name+"/"+folder_name+str(file_number)
      kk.takePicture(camera, file_name)
      file_number+=1
    else:
      file_number=0
      return('/home/pi/Desktop/%s' % folder_name)


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
        queue_weight.put(kk.readScale_grams())
        time.sleep(1)

def read_water():
    while True:
        queue_water.put(kk.measureDistance())
        time.sleep(1)


def save_reading():
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
            event_camera.set()
            is_eating=True
            curr_water_bowl=test_water
            curr_food_bowl=test_food
        else:
            if is_eating:
                is_eating=False
                now=datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                curr_water_percent=(full_water_bowl/curr_water_bowl)*100
                curr_food_percent=(full_food_bowl/curr_food_bowl)*100
                with open(DATA_FILE, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([str(curr_water_percent), str(curr_food_percent), dt_string])

def camera_prediction():
     event_camera.wait()
     now=datetime.now()
     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
     cap = kk.takePicture(camera, "prediction")
     -, img = cap.read()
     res,name = tm.predict(img)
     idx = np.argmax(res)
     with open(PREDICTION_FILE, 'a', newline='') as file:
        writer = csv.write(file)
        writer.writerow([str(name), str(idx),dt_string])
     event_camera.clear()
