#!/usr/bin/python

import sys
import json
import os
import time
import paho.mqtt.client as mqtt
import logging
import libspacy
import libgrams
import libwordnet
import numpy as np
import numpy
from sklearn import linear_model
import pickle

logging.basicConfig(filename='/tmp/listener.log', level=logging.INFO,format='%(asctime)s %(message)s')

def on_message_new_request(mosq, obj, msg):
  global mqttc
  payload = str(msg.payload)
  logging.info("NEW REQUEST: "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
  json_obj = json.loads(payload)
  logging.info(json_obj)
  exp_id = str(json_obj['id'])
  title = str(json_obj['title'])
  logging.info("id=" + exp_id)

  bizarre=97
  bizarre = get_bizarre_proba(title)

  response_json = {'id':exp_id, 'title':title, 'bizarre':bizarre}

  response = json.dumps(response_json)

  logging.info("Sending response: "+response)
  topic=exp_id
  mqttc.publish(topic=topic, payload=response)


#the main method kind of
countries = []
stopwords=[u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now', u'd', u'll', u'm', u'o', u're', u've', u'y', u'ain', u'aren', u'couldn', u'didn', u'doesn', u'hadn', u'hasn', u'haven', u'isn', u'ma', u'mightn', u'mustn', u'needn', u'shan', u'shouldn', u'wasn', u'weren', u'won', u'wouldn']


def get_bizarre_proba(title):
  print "Entered bizarre proba with title=", title

  #load the picke file
  pickle_file = 'log_reg_model.pickle'
  logistic = pickle.load( open( pickle_file, "rb" ) )

  X_test=[]

  print "Extracting features"
  title = ''.join([i if ord(i) < 128 else ' ' for i in title])
  features = generate_features(title)
  X_test.append(features)

  num_features = len(features)
  print "#features=", num_features

  print"Predicting through logistic regression"
  y_pred = logistic.predict_proba(X_test)

  bizarre=round(100*y_pred[0][1])
  return bizarre
 

def generate_features(title):
  features=[]
  f1=structural_and_punctuation(title)
  f2=linguistic(title)
  f3=word_sentence(title)
  f4=libspacy.get_vector(title)
  return f1+f2+f3+f4.tolist()

def structural_and_punctuation(title):
  features=[]
  #First feature is the sentence structure ie words in the title
  words=title.split(' ')
  num_words = len(words)
  features.append(num_words)

  #Number of stop words
  stop_bool = [ 1 if w in stopwords else 0 for w in words]
  num_stop = sum(stop_bool)
  features.append(num_stop)

  #Average word length
  avg_word_len = float(len(title))/num_words
  features.append(avg_word_len)

  #Presence of ellipsis
  if '..' in title:
    f=1
  else:
    f=0

  #features.append(f) #f3

  #Quoted characters
  num_quotes = title.count("'")
  if num_quotes >=2:
    num_quotes = 1
  features.append(num_quotes)

  #Presence of colon character
  colon = title.count(':')
  features.append(colon) #f5

  if '!' in title:
    features.append(1)
  else:
    features.append(0)
  if '?' in title:
    features.append(1)
  else:
    features.append(0)
  if '-' in title:
    features.append(1)
  else:
    features.append(0)

  return features



def linguistic(title):
  most_rep_sub_w=['man', 'police', 'woman', 'who', 'it', 'you', 'court', 'he', 'dog', 'that', 'i', 'men', 'women', 'china', 'thief', 'driver', 'boy', 'thieves', 'study', 'judge', 'city', 'town', 'couple', 'scientists', 'museum', 'students', 'firm', 'leader', 'they', 'fans', 'mayor', 'official', 'dogs', 'minister', 'student', 'cat', 'we', 'she', 'putin', 'workers']
  most_rep_sub_n=['it', 'i', 'that', 'you', 'who', 'india', 'he', 'khan', 'trump', 'we', 'obama', 'us', 'man', 'modi', 'police', 'she', 'clinton', 'this', 'bjp', 'pakistan', 'people', 'dhoni', 'google', 'woman', 'court', 'here', 'congress', 'they', 'president', 'singh', 'kohli', 'china', 'government', 'apple', 'shah', 'what', 'facebook', 'one', 'microsoft', 'film']
  features=[]
  f=0
  #First feature is if any common subject from weird category is present in the title or not
  words=title.lower().split(' ')
  num_words = len(words)
  for word in words:
    if word in most_rep_sub_w:
      f=1
      break
  features.append(f)
  for word in words:
    if word in most_rep_sub_n:
      f=1
      break
  features.append(f) #f10


  #Possessives
  possessives = ['i', 'he','she',  'you', 'they', 'them', 'him', 'her', 'their',
          'these', 'those', 'this', 'that']
  f=0
  for word in title.lower().split(' '):
    if word in possessives:
      f=1
      break
  features.append(f) #f11

  #Capitalized words
  #Num capitalized words
  num_cap_words =sum( [word.upper()==word and word.lower() !=word for word in words])
  features.append(num_cap_words) #f12

  #Presence of question forms
  q_words = ['what', 'which', 'who', 'when', 'whose', 'whom', 'how', 'where']
  f=0
  for word in title.lower().split(' '):
    if word in q_words:
      f=1
      break
  features.append(f) #f13


  return features

def word_sentence(title):
  features=[]
  #Pos counts
  pos_counts = libspacy.get_pos_counts(str(title))
  features +=pos_counts

  #Number of animals and human body parts
  nouns = libspacy.get_nouns(title)
  animals = [w for w in nouns if libwordnet.is_animal(w) ]
  num_animals = len(animals)
  parts = [w for w in nouns if libwordnet.is_body_part(w) ]
  num_parts = len(animals)

  features.append(num_animals)
  features.append(num_parts)

  #NEs in first and second halves
  total_f = total_s = 0
  nes = libspacy.get_nes(' '.join(title.split(' ')[:int(len(title.split(' '))/2)]))
  total_f +=len(nes)
  nes = libspacy.get_nes(' '.join(title.split(' ')[int(len(title.split(' '))/2):]))
  total_s +=len(nes)

  features.append(total_f)
  features.append(total_s)

  #is NVN phrase present
  nvps = libspacy.get_noun_verb_pos(title)
  if 'NVN' in nvps:
    f=1
  else:
    f=0
  features.append(f)

#Country as feature
  count =0
  for country in countries:
    if country in title.lower():
      count = count+1
  features.append(count)
  f=0
  for verb in freq_verbs:
    if verb in title.lower():
      f=1
      break
  features.append(f)

  num_noun_phrases=len(libspacy.get_noun_phrases(title))
  features.append(num_noun_phrases)
  return features
def load_countries():
  fp = open('countries.txt', 'r')
  for line in fp:
    countries.append(line.strip().lower())
  #print countries
  return countries
freq_verbs = ['say', 'found', 'arrest',  'accuse',
        'sue', 'jail', 'caught',
        'stolen', 'lose', 'survive',
        'die', 'kill', 'apologize', 'end', 'save',
        'eat', 'driv', 'ban', 'leave', 'keep', 'win',
        'steal', 'stop', 'nab', 'ban', 'miss', 'sentence', 'sue',
        'fire', 'protest', 'plead', 'call', 'slam', 'visit', 'hit', 'reject',
        'accuse', 'join', 'seek', 'offer', 'led', 'discuss', 'need', 'leave',
        'bring', 'fight', 'continue', 'announce', 'protest', 'vow',
        'condemn', 'refuse', 'write', 'wound', 'lead', 'member','quit',
        'withdraw',
        'porn', 'sex', 'condom', 'nude', 'dead', 'male', 'female', 'mistake'
        'sink', 'food', 'sky', 'auction', 'pay', 'forgot',  ]


mqttc = mqtt.Client()
def main():
  global mqttc

# Add message callbacks that will only trigger on a specific subscription match.
  mqttc.message_callback_add("request", on_message_new_request)
  mqttc.connect("localhost", 1883, 60)
  mqttc.subscribe("request", 0)
  print "Subscribed to request"

  mqttc.loop_forever()


if __name__ == "__main__":
  load_countries()
  #title='Russian parliament grants Putin right to use military force in Syria'
  #print generate_features(title)

  main() 
