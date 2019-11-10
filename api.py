import flask
from flask import request, jsonify, render_template, redirect
import time
import sqlite3
# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend
from imutils import build_montages
import cv2
import numpy as np
from flask_cors import CORS
import io
import webbrowser
import webbrowser

import os
from urllib.request import pathname2url

app = flask.Flask(__name__)
CORS(app)

conn = sqlite3.connect('database.db')
print("Opened database successfully")

try:
    conn.execute('CREATE TABLE MyUsers (firstName TEXT, lastName TEXT, ins_ID TEXT, city TEXT, dob TEXT, date TEXT)')
except:
    pass
try:
    conn.execute('CREATE TABLE CreateUser (email TEXT, password TEXT, reference TEXT)')
except:
    pass


@app.route('/prediction', methods=['POST'])
def api_image():
    # Database
    firstName = request.args['fname']
    lastName = request.args['lname']
    ins_ID = request.args['ins_ID']
    city = request.args['city']
    dob = request.args['dob']
    date1 = request.args['date']
    print("firstName: ",firstName)
    print("lastName: ", lastName)
    print("city: ", city)
    print("dob: ", dob)
    print("date: ", date1)

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO MyUsers VALUES(?, ?, ? ,? ,? ,?)',(firstName, lastName, ins_ID, city, dob, date1))

        con.commit()
        print("Record successfully added")

    model_name = request.args["model"]
    photo = request.files['photo']
    in_memory_file = io.BytesIO()
    photo.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    orig = cv2.imdecode(data, color_image_flag)
    model_path = ""

    # load the pre-trained network
    print("[INFO] loading pre-trained network...")
    if model_name in "cancer":
        print("cancer model loaded")
        model_path = r"models/breast_cancer_model.model" # Please enter the path for breast-cancer model

    elif model_name in "malaria":
        print("Maalaria model loaded")
        model_path = r"models/malaria_model.model" # Path for Malaria model

    elif model_name in "spiral":
        print("Spiral model loaded")
        model_path = r"models/spiral_model.model" # Path for Spiral model


    elif model_name in "wave":
        print("Wave model loaded")
        model_path = r"models/wave_model.model" # Path for wave model

    model = load_model(model_path)
    # initialize our list of results
    results = []

    # pre-process our image by converting it from BGR to RGB channel
    # ordering (since our Keras mdoel was trained on RGB ordering),
    # resize it to 64x64 pixels, and then scale the pixel intensities
    # to the range [0, 1]
    image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (48, 48))
    image = image.astype("float") / 255.0

    # order channel dimensions (channels-first or channels-last)
    # depending on our Keras backend, then add a batch dimension to
    # the image
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # make predictions on the input image
    pred = model.predict(image)

    print("pred: ", pred)
    pred = pred.argmax(axis=1)[0]

    # an index of zero is the 'parasitized' label while an index of
    # one is the 'uninfected' label
    label = "UnInfected" if pred == 0 else "Infected"
    color = (0, 0, 255) if pred == 0 else (0, 255, 0)

    # resize our original input (so we can better visualize it) and
    # then draw the label on the image
    orig = cv2.resize(orig, (128, 128))
    cv2.putText(orig, label, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                color, 2)

    # add the output image to our list of results
    results.append(orig)

    # show the output montage
    #cv2.imshow("Results", montage)
    #cv2.waitKey(0)

    # else:
    #     return "Error: No image address field provided."

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    res = {}

    if pred == 1:
        res = {"Prediction":"1"}
        print(res)
    else:
        res = {"Prediction":"0"}
        print(res)

    backend.clear_session()

    return jsonify(res)

@app.route('/login',methods=['POST'])
def login():
    email = request.args['email']
    password = request.args['password']
    print(email)
    print(password)


    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select * from CreateUser where email = \'{}\' and password =\'{}\'".format(email,password))

        if len(cur.fetchall()) > 0:
            status ={'OK': "1"}
            print("Login Success")
        else:
            status = {'OK':"2"}
            print("Login Error")
    backend.clear_session()

    return jsonify(status)

@app.route('/register',methods=['POST'])
def register():
    email = request.args['email']
    password = request.args['pwd1']
    reference = request.args['reference']
    print(email)
    print(password)
    print(reference)


    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute('INSERT INTO CreateUser VALUES(?, ?, ?)',(email, password, reference))

        con.commit()
        print("Record successfully added")

    return jsonify({'nw':"1"})


# Python 3.x

url = 'file:{}'.format(pathname2url(os.path.abspath('front-end/index.html')))
webbrowser.open(url)

app.run()



