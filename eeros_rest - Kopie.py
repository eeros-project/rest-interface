from app import app, crossd, auth
from flask import Flask, Response, request, session, request, redirect, jsonify
from eeros_mock import EEROS

import time, math, ConfigParser, os, json
from settings import APP_STATIC
from random import randrange


e = EEROS("/dev/eeduro")
e.open()



##BEGIN TEST SECTION************************************************

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


"""get test signal"""
@app.route('/eeros/signals/get_test/test/')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_signals_test():
    data = []
    l=x.get()
    data.append({"label" : "Test" ,"data" : l })
    return jsonify({"signals" : data})



"""get test signals from txt files"""
@app.route('/eeros/signals/get_test/<filenames>')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_test_signals_get(filenames):
    data = []
    fileList = filenames.split(",")
    for i in range(len(fileList)):
        with open(os.path.join(APP_STATIC , "test_data\\" + fileList[i] + ".txt")) as file:
            l = eval(file.read())
            file.close
            for key in sorted(l.iterkeys()):
                data.append({"label" : key ,"data" : l[key] })

    return jsonify({"signals" : data})


"""Get Test Log messages"""
@app.route('/eeros/logs/get_test')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_logs_get_test():
    data=[]
    logsColor=["#FF0000", "#FF00FF", "#FFB6FF", "#FFFF00", "#00FF00", "#00FFFF", "#00BBFF", "#DADADA", "#FFFFFF"]
    logs = e.log.get()
    i = randrange(0,7)

    color_index = logs[i][2]
    if (color_index > 7):
        color_index = 8
    data.append({"recid" : i ,"timestamp" : time.time(), "cat" : logs[i][1], "sev" : logs[i][2], "message" : logs[i][3], "style" : "background-color: " + logsColor[color_index]}) 
    return jsonify({"records" : data})

##END TEST SECTION************************************************






"""Login"""
@app.route('/connection')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def connect():
    config = ConfigParser.ConfigParser()
    config.read('EEROS.cfg')
    name = config.get('EEROS', 'name', 0)
    return jsonify({"robotname" : name })




#list of signals
@app.route('/eeros/signals/list')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def signals_list():
    data = []
    l = e.signals.list()
    for key in sorted(l.iterkeys()):
        data.append({"recid" : key ,"unit" : l[key] }) 
    return jsonify({"records" : data})


#subscribe signals
#@app.route('/eeros/signals/subscribe/<signals>')
@app.route('/eeros/signals', methods = ['GET', 'PUT', 'DELETE'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_signals():
    if request.method == 'GET':     #get signal data
        data = []
        l=e.signals.get()
        for key in sorted(l.iterkeys()):
                data.append({"label" : key ,"data" : l[key] })
        return jsonify({"signals" : data})

    if request.method == 'PUT':     #subscribe signals
        content = request.json
        print content
        #return jsonify({ "signals" : content })

    #signalList = signals.split(",")
    #l=e.signals.subscribe(signalList)
    #return jsonify({ "signals" : l })



#get signals
@app.route('/eeros/signals/get')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_signals_get():
    data = []
    l=e.signals.get()
    for key in sorted(l.iterkeys()):
            data.append({"label" : key ,"data" : l[key] })
    return jsonify({"signals" : data})




#current safety level

@app.route('/eeros/levels', methods = ['GET'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_levels_current():
    #Test with random data
    i = randrange(0,3)
    e.levels.index = i
    
    data = e.levels.current()
    return jsonify( {"name" : data[0] ,"description" : data[1]} )


#Get Log messages
@app.route('/eeros/logs')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_logs_get():
    data=[]
    logsColor=["#FF0000", "#FF00FF", "#FFB6FF", "#FFFF00", "#00FF00", "#00FFFF", "#00BBFF", "#DADADA", "#FFFFFF"]
    logs = e.log.get()

    for i in range(len(logs)):
        color_index = logs[i][2]
        if (color_index > 7):
            color_index = 8
        data.append({"recid" : i ,"timestamp" : logs[i][0], "cat" : logs[i][1], "sev" : logs[i][2], "message" : logs[i][3], "style" : "background-color: " + logsColor[color_index]}) 
    return jsonify({"records" : data})




#List of events
@app.route('/eeros/events/list')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_events_list():
    data = []
    l = e.events.list()
    for key in sorted(l.iterkeys()):
        data.append({"recid" : key ,"description" : l[key] }) 
    return jsonify({"records" : data})


#Trigger event
@app.route('/eeros/events/trigger/<event>')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_events_trigger(event):
    success = e.events.trigger(event)
    return jsonify({"success" : success})


#List of sequences
@app.route('/eeros/sequences/list')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_sequences_list():
    data = []
    l=e.sequences.list()
    #for k, v in l.items():
    for k in l:
        elements = {}
        elements["recid"] = k
        elements.update({"description" : l[k]["description"]})
        if "return" in l[k]:
            elements.update({"return" : l[k]["return"]})
        if "param" in l[k]:
            elements.update({"param" : l[k]["param"]})

        data.append(elements)
    return jsonify({"records" : data })



#Start sequence
@app.route('/eeros/sequences/start/<sequence>')
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_sequence_start(sequence):
    seq = sequence.split("%@%")
    seqName = seq[0]
    params = seq[1:]
    l=e.sequences[seqName](params)
    return jsonify({"success" : 'ok'})

  
