from flask import Flask, render_template, redirect,request, send_file
from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os
import app_weight
from csv import csv,DictReader
from datetime import time,date, datetime, timedelta

#pet name and aged are saved in CSV file
petlist = "pets.csv"

with open(petlist, 'w', newline='') as file:
        writer = csv.writer(file)
        field = ["Pet Name", "Pet Age"]
        writer.writerow(field)

app = Flask(__name__, static_folder='assets')

@app.route("/")
def home():
    return redirect("/home")

@app.route("/home")
def home_template():
    with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
    return render_template("home.html", myPets=tuple_of_dict)


#recieves pet name and age from "addpet.html" and saves it to "pets.csv"
@app.route("/addpet", methods=['POST','GET'])
def add_pet():
    if request.method=="POST":
        petname = request.form['p_name']
        petage = request.form['p_age']
        with open(petlist, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([petname, petage])
        return redirect("/home")
    return render_template("addpet.html")

#function for taking photos
@app.route("/takephotos", methods=['POST','GET'])
def take_photos():
    if request.method=="GET":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
        return render_template("takephotos.html", myPets=tuple_of_dict)
    if request.method=="POST":
        petname=request.form['p_name']
        app_weight.make_folder(petname)
        for i in range (0,29,1):
            app_weight.camera_training(petname, False)
            time.sleep(2)
        app_weight.camera_training(petname, True)

#function for downloading photos
@app.route("/download")
def download():
    target = '/home/pi/Desktop/Pictures'
    stream = BytesIO()
    with ZipFile(stream, "w") as zf:
        for file in glob(os.path.join(target, '*.sql')):
            zf.write(file, os.path.basename(file))
            stream.seek(0)
    return send_file(stream, as_attachment=True, downloaded_name='pictures.zip')


app.config["UPLOAD_FOLDER"] = '/home/pi/Kibble-Kounter1/teachablemachinepython/tflite_model/'

#function for facial recognition
@app.route("/facialrecognition", methods=['POST','GET'])
def facial_recognition():
    if request.method=="GET":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
        return render_template("facialrecognition.html", myPets=tuple_of_dict)
    if request.method=="POST":
        files=request.files.getlist['file']
        for file in files:
            filename = file.secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+filename)
        return redirect("/home")

#recieves pets name, makes file to collect information for the pets bowl in and zeroes the sensors for that pets bowl
@app.route("/startsetup", methods=['POST', 'GET'])
def start_set_up():
    if request.method=="GET":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
        return render_template("startsetup.html", myPets=tuple_of_dict)
    if request.method=="POST":
        petname=request.form['p_name']
        DATA_FILE = petname+".csv"
        app_weight.make_folder(DATA_FILE)
        #petname can eventually be used to determine which sensors to zero in the following line
        app_weight.zero_sensors()
        return render_template("finishsetup.html")
    
#recieves pets name, tests sensors for that pets bowl  
@app.route("/finishsetup", methods=['POST', 'GET'])
def finish_set_up():
    if request.method=="GET":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
        return render_template("finishsetup.html", myPets=tuple_of_dict)
    if request.method=="POST":
        #obtain petname from dropdown menu
        petname=request.form['p_name']
        #petname can eventually be used to determine which sensors to test in the following line
        app_weight.test_sensors()
        return render_template("home.html")

#gets pets name, starts tracking for that pets bowl sensors
@app.route("/startdevice", methods=['POST', 'GET'])
def start_device():
    if request.method=="GET":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
        return render_template("startdevice.html", myPets=tuple_of_dict)
    if request.method=="POST":
        petname=request.form['p_name']
        #pets name is used to start device ????????? ARIN
        return render_template("home.html")

@app.route("/data", methods=['POST', 'GET'])
def data():
    if request.method=="GET":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
        return render_template("data.html", myPets=tuple_of_dict)
    if request.method=="POST":
        petname=request.form['p_name']
        time_range=request.form['range']

        #files can be obtained this way: directly from the pets bowl data without facial recognition:
        with open(petname+".csv", 'r') as f:
            dict_reader = DictReader(f)
            list_of_dict = list(dict_reader) 

        #files can be obtained a second way: parse through all bowls and see which one predicted pet with facial recognition:
        """ list_of_dict1 = []
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            list_of_pets = list(dict_reader)
        for x in list_of_pets:
            with open(x["Pet Name"]+".csv", 'r') as f:
                dict_reader = DictReader(f)
                list_of_dict2 = list(dict_reader) 
            for y in list_of_dict2:
                if y['predicted_name'] != petname:
                    y.remove(y)
            if len(list_of_dict2)!=0:
                list_of_dict1.extend(list_of_dict2) """

        today = datetime.now().replace(microsecond=0)
        dayago = (datetime.now().replace(microsecond=0)) - timedelta(days=1)
        weekago = (datetime.now().replace(microsecond=0)) - timedelta(days=7)
        monthago = (datetime.now().replace(microsecond=0)) - timedelta(weeks=4)

        if time_range == "12":
            for lines in list_of_dict:
                if not(dayago <= lines['time'] <= today): 
                    lines.remove(lines)
        if time_range == "13":
            for lines in list_of_dict:
                if not(weekago <= lines['time'] <= today): 
                    lines.remove(lines)
        if time_range == "14":
            for lines in list_of_dict:
                if not(monthago <= lines['time'] <= today): 
                    lines.remove(lines)
        if time_range == "15":
            for lines in list_of_dict:
                if not(lines['time'] <= today): 
                    lines.remove(lines)
        
        tuple_of_dict = tuple(list_of_dict)

        return render_template("data.html", myData=tuple_of_dict)    
         


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
