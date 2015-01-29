from app import app, crossd, auth
from flask import Flask, request, session, jsonify
from eeros_mock import EEROS
import datetime, time, math, ConfigParser, os, json
from settings import APP_STATIC
from random import randrange

try:
    from flask.ext.cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask.ext.cors import CORS

#Allow Cross Domain request    
CORS(app, resources=r'/eeros/*', allow_headers='Content-Type')



e = EEROS("/dev/eeduro")
e.open()



##BEGIN TESTDATA SECTION************************************************

from time import sleep
from array import *
from thread import start_new_thread

class RingBuffer:
    def __init__(self,size_max):
        self.max = size_max
        self.data = []
    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.data.pop(0)
    def get(self):
        """ return a list of elements"""
        l = len(self.data)
        res = self.data[:l]
        self.data = self.data[l+1 :]
        return res



def generate_data():
    while True:
        t = (time.time(), randrange(100))
        x.append(t)
        sleep(0.001)

        
x=RingBuffer(2000)
start_new_thread(generate_data,())

##END TESTDATA SECTION************************************************


@app.route('/eeros/test/levels', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def test_levels_current():
    if request.method == 'GET':
        i = randrange(0,3)
        e.levels.index = i
        
        data = e.levels.current()
        return jsonify( {"name" : data[0] ,"description" : data[1]} )



@app.route('/eeros/test/logs', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def test_logs():
    data=[]
    logsColor=["#FF0000", "#FF00FF", "#FFB6FF", "#FFFF00", "#00FF00", "#00FFFF", "#00BBFF", "#DADADA", "#FFFFFF"]
    logs = e.log.get()
    i = randrange(0,7) 

    color_index = logs[i][2]
    if (color_index > 7):
        color_index = 8
    t=datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    data.append({"recid" : i ,"timestamp" : t, "cat" : logs[i][1], "sev" : logs[i][2], "message" : logs[i][3], "style" : "background-color: " + logsColor[color_index]}) 
    return jsonify({"records" : data})


#Signal test ringbuffer
@app.route('/eeros/test/signals/random', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def test_random():
    data = []
    l=x.get()
    data.append({"label" : "Test" ,"data" : l })
    return jsonify({"signals" : data})



#Signal test with txt files"""
@app.route('/eeros/test/signals/<filenames>', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def test_signals(filenames):
    data = []
    fileList = filenames.split(",")
    for i in range(len(fileList)):
        with open(os.path.join(APP_STATIC , "test_data\\" + fileList[i] + ".txt")) as file:
            l = eval(file.read())
            file.close
            for key in sorted(l.iterkeys()):
                data.append({"label" : key ,"data" : l[key] })

    return jsonify({"signals" : data})












