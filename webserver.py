from flask import Flask, render_template
from flask import request, jsonify
from flask_cors import CORS
#import cv2
import requests
import uuid
import json
import os
import time
#import matplotlib.pyplot as plt
# os.system('snort -A console -i eth0 -c /etc/snort/snort.conf -l /var/log/snort -K ascii ') 
app = Flask(__name__)
CORS(app)

@app.before_request
def log_request_info():
    user = uuid.uuid4().hex
    f = open("connectionrequests.txt", "a")
    # f.write("user :"+user+str(r.text))
    f.write("user : ")
    f.write(str(user))
    f.write("\n")
    f.write('Headers: ')
    f.write(str(request))
    f.write('Body: ')
    f.write(str(request.get_data()))
    f.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creds')
def creds():
    f = open("data.json", "r")
    return jsonify(f.read())

@app.route('/screenshot/')
def my_link():
    user = uuid.uuid4().hex
    capture = cv2.VideoCapture(0)    
    if capture.isOpened():
        frame = capture.read()

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    directory = os.getcwd() + "/images"
    os.chdir(directory)
    #print(os.listdir(directory)) 
    filename = 'Intruder '+user+'.jpg'
    cv2.imwrite(filename, image)

@app.route('/submit')
def submit():
    user = uuid.uuid4().hex
    geoip_data = 'https://ipinfo.io/'
    r = requests.get(geoip_data)
    f = open("location.txt", "a")
    # f.write("user :"+user+str(r.text))
    f.write("user : ")
    f.write(str(user))
    f.write(str(r.text))
    f.write("\n")
    f.close()
    return render_template('index.html')
app.run(host='0.0.0.0')

