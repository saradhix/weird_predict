#!/usr/bin/python

import sys
import json
import os
import time
import paho.mqtt.client as mqtt
import logging

logging.basicConfig(filename='/tmp/listener.log', level=logging.INFO,format='%(asctime)s %(message)s')

def on_message_new_request(mosq, obj, msg):
  payload = str(msg.payload)
  logging.info("NEW REQUEST: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
  json_obj = json.loads(payload)
  logging.info(json_obj)
  exp_id = str(json_obj['id'])
  title = str(json_obj['title'])
  logging.info("id=" + exp_id)

  bizarre=97

  response_json = {'id':exp_id, 'title':title, 'bizarre':bizarre}

  response = json.dumps(response_json)

  logging.info("Sending response: "+response)
  mqttc.publish(topic="response",payload=response)




mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("request", on_message_new_request)
#mqttc.message_callback_add("old", on_message_old_experiment)
#mqttc.on_message = on_message
mqttc.connect("localhost", 1883, 60)
mqttc.subscribe("request", 0)

mqttc.loop_forever()

