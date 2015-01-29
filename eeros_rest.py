from settings import APP_STATIC
from app import app, auth, crossd
from flask import Flask, Response, session, request, jsonify
from eeros_mock import EEROS

import datetime, time, math, ConfigParser, os, json

try:
    from flask.ext.cors import CORS
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



@app.route('/connection/<data>', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_connect(data):
    login = data.split(",")
    username = login[0]
    password = login[1]
    #auth.username = username
    #auth.password = password
    if not auth.check_auth(username, password):
        return jsonify({"login" : False })
    else:       
        config = ConfigParser.ConfigParser()
        config.read('EEROS.cfg')
        robotname = config.get('EEROS', 'name', 0)
        return jsonify({"robotname" : robotname })


#current safety level
@app.route('/eeros/levels', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_levels_current():
    if request.method == 'GET':
        data = e.levels.current()
        return jsonify( {"name" : data[0] ,"description" : data[1]} )


#Get Log messages
@app.route('/eeros/logs', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_logs_get():
    if request.method == 'GET':
        data=[]
        logsColor=["#FF0000", "#FF00FF", "#FFB6FF", "#FFFF00", "#00FF00", "#00FFFF", "#00BBFF", "#DADADA", "#FFFFFF"]
        logs = e.log.get()
        for i in range(len(logs)):
            color_index = logs[i][2]
            time = datetime.datetime.fromtimestamp(int(logs[i][0])).strftime('%H:%M:%S')
            if (color_index > 7):
                color_index = 8
            data.append({"recid" : i ,"timestamp" : time, "cat" : logs[i][1], "sev" : logs[i][2], "message" : logs[i][3], "style" : "background-color: " + logsColor[color_index]}) 
        return jsonify({"records" : data})




#list of signals
@app.route('/eeros/signals/list', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def signals_list():
    if request.method == 'GET':
        data = []
        l = e.signals.list()
        for key in sorted(l.iterkeys()):
            data.append({"recid" : key ,"unit" : l[key] }) 
        print data
        return jsonify({"records" : data})


#subscribe/get/unsubscribe signals
@app.route('/eeros/signals/', methods = ['GET', 'PUT', 'DELETE', 'OPTIONS'])
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
        signalList = request.get_json(force=True)
        l=e.signals.subscribe(signalList["signals"])
        return jsonify({ "signals" : l })

    if request.method == 'DELETE':     #unsubscribe signals
        signalList = request.get_json(force=True)
        #l=e.signals.unsubscribe(signalList["signals"])



#List of events
@app.route('/eeros/events/list', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_events_list():
    data = []
    l = e.events.list()
    for key in sorted(l.iterkeys()):
        data.append({"recid" : key ,"description" : l[key] }) 
    return jsonify({"_links": [{"rel": "self", "href": "/eeros/events/list"},
                               {"rel": "sequences", "href": "/eeros/sequences/list"}],
                    "records" : data})







#Trigger event
@app.route('/eeros/events', methods = ['PUT', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_events_trigger():
    if request.method == 'PUT':             #trigger event
        data = request.get_json(force=True)
        success = e.events.trigger(data["event"])
        return jsonify({"success" : success})



#List of sequences
@app.route('/eeros/sequences/list', methods = ['GET', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_sequences_list():
    data = []
    l=e.sequences.list()
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
@app.route('/eeros/sequences', methods = ['PUT', 'OPTIONS'])
@crossd.crossdomain(origin='*')
#@auth.requires_auth
def api_sequences_start():
    if request.method == 'PUT':         #start sequence
        data = request.get_json(force=True)
        seqName = data["seqName"]
        seq = data["params"]
        params = seq[0:]

        l=e.sequences[seqName](params)
        return jsonify({"success" : True})

          
