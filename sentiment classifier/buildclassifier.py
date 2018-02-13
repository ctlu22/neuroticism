#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import pickle
import re
import time
import random
from time_limit import *
import traceback
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
import nltk
import csv

### GLOBALS FOR THE MODULE ###

classifier = None
main_feautures = None

### CODE FOR FEATURE EXTRACTION FROM TWEET TEXT  ###

gt_replace = re.compile(r'&gt;')
lt_replace = re.compile(r'&lt;')
quote_replace = re.compile(r'&quot;')
amp_replace = re.compile(r'&amp;')
 
mention_replace = re.compile(r'@\w+')
link_replace = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
repeat_reduce = re.compile(r'(\w)\1{2,}')
punc_reduce = re.compile(r'(\W)\1+')
punc_break_1 = re.compile(r'(\s\W)(\w{2,})')
punc_break_2 = re.compile(r'(\w{2,})(\W\s)')
stopwords_dict = [(x, True) for x in stopwords.words()]

def CreateFeatures(text, main_features = None):
  
  tokens = []

  text = gt_replace.sub(r'>', text)
  text = lt_replace.sub(r'<', text)
  text = quote_replace.sub(r'"', text)
  text = amp_replace.sub(r'&', text)
  
  # replace mentions with a dummy string
  (text, count) = mention_replace.subn(r'', text)
  if count > 0:
    tokens.append("<MENTION>")
  # replace links with a dummy string
  (text, count) = link_replace.subn(r'', text)
  if count > 0:
    tokens.append("<LINK>")

  text = text.lower()
  # shorten long spans of repeated word chars to two ("sooooo" -> "soo")
  text = repeat_reduce.sub(r'\1\1', text)
  # isolates and reduces long spans of repeated punctuation to a single item (like "...." / " !!!! " / "????")
  text = punc_reduce.sub(r' \1 ', text)
  # break single-character punctuation off of words of size 2 or more 
  text = punc_break_1.sub(r' \1 \2 ', text)
  text = punc_break_2.sub(r' \1 \2 ', text)
  
  tokens = re.split(r'\s+', text)
  tokens = [x for x in tokens if len(x) > 0 and x not in stopwords_dict]
  
  if main_features == None:
    features = dict([(word, True) for word in tokens])
  else:
    features = dict([(word, True) for word in tokens if word in main_features])

  return features



### TRAIN AND SAVE A SENTIMENT CLASSIFIER  ###


def TrainSentimentClassifier(pos_file = 'positive.csv', neg_file = 'negative.csv', occurrence_cutoff = 30, train_percentage = 0.9):
  files = [pos_file, neg_file]
  main_features = {}
  status_features = []
  print "Started reading files..."
  
  for doc in files:
    f = open(doc, 'r')
    class_label = "neg"
    if doc == pos_file:
      class_label = "pos"
    
    fi = csv.reader(f, delimiter = '\t')
    for row in fi:
      # print row
      # print len(row)
      
      if (len(row) != 8):
        print(row)
        continue
      text = row[1]
      feat = CreateFeatures(text)
      for f in feat:
        if f in main_features:
          main_features[f] += 1
        else:
          main_features[f] = 0
      if len(feat) > 0:
        status_features.append((feat, class_label))
  

  main_features_copy = main_features.copy()
  for f in main_features:
    if main_features[f] < occurrence_cutoff:
      del main_features_copy[f]
  main_features = main_features_copy

  f = open("features.lst", "w")
  f.write('\n'.join(list(main_features.keys())))
  f.close()
  print "Got %i Features" % len(main_features)
  
  random.shuffle(status_features)
  train_cut = int(train_percentage * len(status_features))
  train_features = status_features[:train_cut]
  test_features = status_features[train_cut:]

  print "Started to train sentiment classifier..."
  sys.stdout.flush()
  classifier = NaiveBayesClassifier.train(train_features)

  print 'Accuracy:', nltk.classify.util.accuracy(classifier, test_features)
  classifier.show_most_informative_features()
  sys.stdout.flush()

  # save the features and the classifier
  
  f = open("features.pickle", 'w')
  pickle.dump(main_features, f)
  f.close()
  f = open("classifier.pickle", 'w')
  pickle.dump(classifier, f)
  f.close()



### IMPORT THE SENTIMENT CLASSIFIER ###

def LoadSentimentClassifier(feature_file = "features.pickle", classifier_file = "classifier.pickle"):
  global classifier
  global main_features
  
  try:
    print "Importing classifier..."
    sys.stdout.flush()
    
    f = open(feature_file, 'r')
    main_features = pickle.load(f)
    f.close() 

    f = open(classifier_file, 'r')
    classifier = pickle.load(f)
    f.close()

    print "Finished importing."
    sys.stdout.flush()

  except Exception:
    print "Failed."
    print traceback.format_exc()
    sys.exit(1)

    

### FUNCTION TO CLASSIFY TWEET TEXT ###
def ClassifySentiment(text):
  try:
    with time_limit(2):
      feat = CreateFeatures(text, main_features)
      res = classifier.prob_classify(feat)
      probs = dict([(x, res.prob(x)) for x in res.samples()])
      score = probs['pos'] * 2.0 - 1.0
      return score

  except TimeoutException:
    print "Timed out: CreateFeatures for text %s" % text
    return 0.0


# TrainSentimentClassifier()
