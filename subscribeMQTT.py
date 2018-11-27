#    this script forms part of solent air watch data back end
#    it subcribes to an MQTT broker and adds the data to a sqlite database
#    based on example code from https://github.com/eclipse/paho.mqtt.python/tree/master/examples

#    Copyright (C) {2017}  {Joshua Taylor - Solent Air Watch}

import paho.mqtt.client as mqtt
import json
from pprint import pprint  # makes data more pretty



global cursor  # make the database handle available globally
DB_Name = "airwatchData.db"
topicName = "/sniffy/#"
username = 'data'
password = '***'
host = 'awdrop'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topicName, qos=0)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    data = (msg.payload.decode('utf-8'))
    # json.loads
    pprint(data)
    # parse the data to the sql database
##    cursor.execute('''INSERT INTO sniffy(id, timestmp, latitude, longitude, PM10, PM25, PM1)
##                  VALUES(?,?,?,?,?,?,?)''', (data["id"], data["time"], data["latitude"],
##                                             data["longitude"], data["PM10"], data["PM25"], data["PM1"]))
##    db.commit()

client = mqtt.Client()
client.username_pw_set(username, password=password)

# set MQTT call back functions
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)  # (address, port, timeout (sec) )

# set up database connection
##db = sqlite3.connect(DB_Name)
##cursor = db.cursor()
##cursor.execute('''
##    CREATE TABLE IF NOT EXISTS  sniffy(id TEXT, timestmp TEXT,
##                       latitude TEXT, longitude TEXT, PM10 TEXT, PM25 TEXT, PM1 TEXT)
##''')

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()
db.close()  # this will never be executed because of the forever loop - need some exit logic
