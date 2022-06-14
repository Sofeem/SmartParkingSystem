# Inspired and modified from https://github.com/CloudMQTT/python-mqtt-example

import configparser
import paho.mqtt.client as mqtt
import json
import pyrebase



filename = 'data.txt'

firebaseConfig = {'apiKey': "AIzaSyDh8Q85gJ-ra9BBJ8ExCH3XWKFYQpjXcyM",
    'authDomain': "ipawasps.firebaseapp.com",
    'projectId': "ipawasps",
    'databaseURL':"https://ipawasps-default-rtdb.firebaseio.com",
    'storageBucket': "ipawasps.appspot.com",
    'messagingSenderId': "168671824961",
    'appId': "1:168671824961:web:8a8632c6f695b0eb984ac0"
        }




# firebaseConfig = {'apiKey': "AIzaSyCjwZR_wt51-f4z6ChQXKvh-FOdBtigTfE",
#     'authDomain': "parkingdatabasesm.firebaseapp.com",
#     'databaseURL': "https://parkingdatabasesm-default-rtdb.europe-west1.firebasedatabase.app",
#    ' projectId': "parkingdatabasesm",
#     'storageBucket': "parkingdatabasesm.appspot.com",
#     'messagingSenderId': "1008194058793",
#     'appId': "1:1008194058793:web:f752ada4cf970dab60fa38"
#         }
        
 

firebase = pyrebase.initialize_app(firebaseConfig)
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    #payload = str(msg.payload)
#    data_json = json.dumps(msg.payload.decode('utf-8')) 
#    print ("type of final_dictionary", type(data_json)) 
    
    with open('backdata090321.txt', 'a+') as f:
        #json.dump(data_json, json_file)
        f.write(msg.payload.decode('utf-8')+"\r\n")
        
        
    Dictionary = json.loads(msg.payload) 
    data = {'timestamp':Dictionary["tmst"],
            'chan':Dictionary["chan"],
            'rfch':Dictionary["rfch"],
            'freq':Dictionary["freq"],
            'stat':Dictionary["stat"],
            'modu':Dictionary["modu"],
            'datarate': Dictionary["datr"],
            'codr': Dictionary["codr"],
            'lsnr': Dictionary["lsnr"],
            'rssi': Dictionary["rssi"],
            'opts': Dictionary["opts"],
            'size': Dictionary["size"],
            'fcnt': Dictionary["fcnt"],
            'cls': Dictionary["cls"],
            'port': Dictionary["port"],
            'mhdr': Dictionary["mhdr"],
            'appeui': Dictionary["appeui"],
             'seqn': Dictionary["seqn"],   
            'Device_id': Dictionary["deveui"],
            'Gateway_id': Dictionary["gweui"],
            'Time' : Dictionary["time"],
            'Parking_status': Dictionary["payload"][-1],
            'Message_id':Dictionary["_msgid"] } 
    
    DevId= Dictionary["deveui"]
    timestamp = Dictionary["tmst"]
   
    db = firebase.database()
    db.child(DevId).child(timestamp).set(data)
 
    
def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

client = mqtt.Client()
# Assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#client.on_log = on_log

# Get CLOUDMQTT settings from config.ini 
CONFIG = configparser.ConfigParser()
CONFIG.read('config.tmp')
CONFIG_MQTT = CONFIG['Cloudmqtt']
TOPIC = CONFIG_MQTT['TOPIC']
FIRST_MESSAGE = CONFIG_MQTT['MESSAGE']

#MESSAGE

# Connect
client.username_pw_set(CONFIG_MQTT['USER'], CONFIG_MQTT['PASSWORD'])
client.connect(CONFIG_MQTT['CLOUDMQTT_URL'], int(CONFIG_MQTT['PORT']))

# Start subscribe, with QoS level 0
client.subscribe(TOPIC, 0)

# Publish a message
#client.publish(TOPIC, FIRST_MESSAGE)

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = client.loop()
print("rc: " + str(rc))