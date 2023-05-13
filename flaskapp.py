from flask import Flask, render_template, redirect,request, send_file
import flask
from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os
import app_weight
import csv                                                                               
from csv import DictReader                                                               
from datetime import time,date, datetime, timedelta
from werkzeug.utils import secure_filename

#pet name and aged are saved in CSV file
petlist = "pets.csv"

path = './pets.csv'
check = os.path.isfile(path)

if check == True:
	pass
else:
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
        return redirect("/addpet")
    return render_template("addpet.html")

#function for taking photos
@app.route("/takephotos", methods=['POST','GET'])
def take_photos():
    if request.method=="POST":
        petname=request.form['p_name']
        app_weight.make_folder(petname)
        #for i in range (0,29,1):
           # app_weight.camera_training(petname, False)
            #time.sleep(2)
        #app_weight.camera_training(petname, True)
        return redirect("/takephotos")
    with open(petlist, 'r') as f:
        dict_reader = DictReader(f)
        tuple_of_dict = tuple(dict_reader)
    return render_template("takephotos.html", myPets=tuple_of_dict)
            
#function for downloading photos
@app.route("/download")
def download():
    target = '/home/pi/Desktop/pictures'
    stream = BytesIO()
    with ZipFile(stream, "w") as zf:
       for file in glob(os.path.join(target, '*')):
         zf.write(file, os.path.basename(file))
    stream.seek(0)
    return send_file(stream, as_attachment=True, attachment_filename='pictures.zip')


app.config["UPLOAD_FOLDER"] = '/home/pi/Kibble-Kounter1/teachablemachinepython/tflite_model/'
allowed_extensions = set(['txt', 'tflite'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extensions


#function for facial recognition
@app.route("/facialrecognition", methods=['POST','GET'])
def facial_recognition():
    if request.method=="POST":
        f = request.files.getlist('file[]')
        for file in f:
            if file and allowed_file(file.filename):
                print(file.filename)
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect("/home") 
    with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict = tuple(dict_reader)
    return render_template("facialrecognition.html", myPets=tuple_of_dict)


#recieves pets name, makes file to collect information for the pets bowl in and zeroes the sensors for that pets bowl
@app.route("/startsetup", methods=['POST', 'GET'])
def start_set_up():
    if request.method=="POST":
        petname=request.form['p_name']
        DATA_FILE = petname+".csv"
        app_weight.first_setup(DATA_FILE)
        #petname can eventually be used to determine which sensors to zero in the following line
        print("hello1")
        app_weight.zero_sensors()
        print("hello2")
        return redirect("/finishsetup")
    with open(petlist, 'r') as f:
        dict_reader = DictReader(f)
        tuple_of_dict = tuple(dict_reader)
    return render_template("startsetup.html", myPets=tuple_of_dict)
    
#recieves pets name, tests sensors for that pets bowl  
@app.route("/finishsetup", methods=['POST', 'GET'])
def finish_set_up():
    if request.method=="POST":
        #obtain petname from dropdown menu
        petname=request.form['p_name']
        #petname can eventually be used to determine which sensors to test in the following line
        app_weight.test_sensors()
        return redirect("/home")
    with open(petlist, 'r') as f:
        dict_reader = DictReader(f)
        tuple_of_dict = tuple(dict_reader)
    return render_template("finishsetup.html", myPets=tuple_of_dict)

#gets pets name, starts tracking for that pets bowl sensors
@app.route("/startdevice", methods=['POST', 'GET'])
def start_device():
    if request.method=="POST":
        petname=request.form['p_name']
        #pets name is used to start device ????????? ARIN
        app_weight.start_device(petname)
        return redirect("/home")
    with open(petlist, 'r') as f:
        dict_reader = DictReader(f)
        tuple_of_dict = tuple(dict_reader)
    return render_template("startdevice.html", myPets=tuple_of_dict)

@app.route("/data", methods=['POST', 'GET'])
def data():
    if request.method=="POST":
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            tuple_of_dict1 = tuple(dict_reader)
        
        petname=request.form['p_name']
        time_range=request.form['range']

        #files can be obtained this way: directly from the pets bowl data without facial recognition:
        with app_weight.lock_csv:
            with open(petname+".csv", 'r') as f:
                dict_reader = DictReader(f)
                list_of_dict = list(dict_reader) 

        #files can be obtained a second way: parse through all bowls and see which one predicted pet with facial recognition:
        """ list_of_dict0 = []
        with open(petlist, 'r') as f:
            dict_reader = DictReader(f)
            list_of_pets = list(dict_reader)
        for x in list_of_pets:
            with open(x["Pet Name"]+".csv", 'r') as f:
                dict_reader = DictReader(f)
                list_of_dict01 = list(dict_reader) 
            for y in list_of_dict01:
                if y['predicted_name'] != petname:
                    y.remove(y)
            if len(list_of_dict01)!=0:
                list_of_dict0.extend(list_of_dict01) """

        dayago = (datetime.now().replace(microsecond=0)) - timedelta(days=1)
        weekago = (datetime.now().replace(microsecond=0)) - timedelta(days=7)
        monthago = (datetime.now().replace(microsecond=0)) - timedelta(weeks=4)

        list_of_dict2=[]

        for i in range(len(list_of_dict)):
            if time_range == "12":
                if (datetime.strptime(list_of_dict[i]['time'], "%d/%m/%Y %H:%M:%S")) > dayago:
                    list_of_dict2.append(list_of_dict[i])
            if time_range == "13":
                if (datetime.strptime(list_of_dict[i]['time'], "%d/%m/%Y %H:%M:%S")) > weekago:
                    list_of_dict2.append(list_of_dict[i])
            if time_range == "14":
                if (datetime.strptime(list_of_dict[i]['time'], "%d/%m/%Y %H:%M:%S")) > monthago:
                    list_of_dict2.append(list_of_dict[i])
            if time_range == "15":
                list_of_dict2.append(list_of_dict[i])
        
        tuple_of_dict = tuple(list_of_dict2)

        return render_template("data.html", myPets=tuple_of_dict1, myData=tuple_of_dict)    
    
    with open(petlist, 'r') as f:
        dict_reader = DictReader(f)
        tuple_of_dict = tuple(dict_reader)
    return render_template("data.html", myPets=tuple_of_dict)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
