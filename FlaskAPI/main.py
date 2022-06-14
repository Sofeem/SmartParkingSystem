# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:23:31 2021

@author: newuser
"""


#from flask import Flask
#from flask_restful import Resource, Api, reqparse
#import pandas as pd
#import ast
#import sqlite3
import flask
from flask import request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)
#api = Api(app)
#app.config["DEBUG"] = True

    
@app.route('/', methods = ['GET'])
def home(): 
    return ''' <h1>Distant Reading Archive</h1>
<p> A prototype API for distant reading of science fiction novels. </p>'''  

'''class Sensors(Resource):
    def get(self):
        data = pd.read_csv('latestDataofsensor.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK
        '''
    
@app.route('/api/v1/resources/Sensors/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('SensorData.db')
    cur = conn.cursor()
    all_sensors = cur.execute('SELECT * FROM SensorData;').fetchall()
    Sensorsjson = json.dumps(all_sensors)
    return jsonify(Sensorsjson)
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


#api.add_resource(Sensors, '/sensors') 
    
@app.route('/api/v1/resources/Sensors', methods=['GET'])
def api_filter():
    query_parameter = request.args
    
    id = query_parameter.get('id')
    conn = sqlite3.connect('SensorData.db')
    cur  = conn.cursor()
    
    results = cur.execute("SELECT * FROM SensorData WHERE DeviceId = '%s'" % id).fetchall()
    #print(results)
    
    Sensorjson = json.dumps(results)
    return jsonify(Sensorjson)
    
@app.route('/api/v1/resources/Date', methods= ['GET'])
def api_dfilter():
    query_parameter = request.args
    
    date = query_parameter.get('date')
    conn = sqlite3.connect('SensorData.db')
    cur  = conn.cursor()
    
    results = cur.execute("SELECT * FROM SensorData WHERE Date = '%s'" % date).fetchall()
    print(results)
    
    Sensorjson = json.dumps(results)
    return jsonify(Sensorjson)

@app.route('/api/v1/resources/DSensor', methods=['GET'])  
def api_dsfilter(): 
    query_parameter = request.args
    
    deviceid = query_parameter.get('deviceid')
    date = query_parameter.get('date')
    
    query = "SELECT * FROM SensorData WHERE"
    to_filter = []
    
    if deviceid:
        query += ' DeviceId = ? AND'
        to_filter.append(deviceid)
    if date:
        query += ' Date = ? AND'
        to_filter.append(date)
    
    conn = sqlite3.connect('SensorData.db')
    cur  = conn.cursor()
    query = query[:-4] + ';'
    #print(query)
    results = cur.execute(query, to_filter).fetchall()
    dictdataset = []
    
    for result in results:
        dictdata = {
            'id' : result[0],
            'date':result[1],
            'time':result[2],
            'Parking_Status':result[3]
            }
        dictdataset.append(dictdata)
        
        print (dictdataset)
        
        
    
    #Sensorjson = json.dumps(dictdataset)
    #print(jsonify(dictdataset))
    return jsonify(dictdataset)
    
#if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)  # run our Flask app