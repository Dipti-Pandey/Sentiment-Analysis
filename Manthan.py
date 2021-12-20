import matplotlib.pyplot as plt
import tweepy as tw
import pandas as pd
import numpy as np
import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
import os
from PIL import Image
import pytesseract
import pathlib
# encoding: utf-8

consumer_key = 'xT4b8LBeN5Ymhwf8ydgtMIEb6'
consumer_secret = 'MUyFZwBWFRJiRtnBCTT5Uxi3Dq3nQUGeoaz5W5NuVwELNJfnY6'
access_token = '884349643894566912-wsOkAhFsmZT6ApgN4XLhwGFvbmK7fe7'
access_token_secret = 'YpOB04oggk9ftTRZPpVjRjU6AauH4bTTCkrq9Gb3bI0V8'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
analyser = SentimentIntensityAnalyzer()
#search_words = "#वसीम_रिज़वी"
date_since = "2021-12-06"
#tweets = tw.Cursor(api.search_30_day, label='testing', query=search_words, ).items(1)

def twitterfunc(keyword,notw):
  notw=int(notw)
  tweetlist = []
  # delete csv file from parent directory
  currentPath = os.getcwd()
  file = os.path.join(currentPath,"Project UI","result.csv")
  if os.path.exists(file):
    f = open(file, 'w+')
    f.close()

  tweets = tw.Cursor(api.search_30_day, label='Testingv2', query=keyword).items(notw)
  for tweet in tweets:
      tweetobject = [
      tweet.user.screen_name,
      GoogleTranslator(source='auto', target='en').translate(tweet.text),
      tweet.created_at,
      analyser.polarity_scores(tweet.text)
      ]
      tweetlist.append(tweetobject)

  fields = ['Username', 'Tweet','Created_Date','Sentiment_Score']

  # name of csv file
  filename = "result.csv"
  currentPath = os.getcwd()
  print(currentPath)
  file = os.path.join(currentPath,"Project UI",filename)
  with open(file, 'w',encoding = "utf-8") as f:
    
    # using csv.writer method from CSV package
    write = csv.writer(f)
    
    write.writerow(fields)
    write.writerows(tweetlist)


pytesseract.pytesseract.tesseract_cmd = r"tesseract.exe"

def img2():
  impath = os.getcwd()
  impath2 = os.listdir(impath)
  for i in impath2:
    imagefile = pathlib.Path(i).suffix
    if imagefile == '.png': 
      img = i 
      print(img)
    elif imagefile == '.jpeg': 
      img = i
      print(img)
    elif  imagefile == '.jpg': 
      img = i
      print(img)
  impath = str(impath)
  img = str(img)
  print(os.path.join(impath,img))
  image = Image.open(os.path.join(impath,img))
  image_to_text = pytesseract.image_to_string(image, lang='eng')
  sentiment = analyser.polarity_scores(image_to_text)
  neg = sentiment.get("neg")
  neu = sentiment.get("neu")
  pos = sentiment.get("pos")
  compound = sentiment.get("compound")
  if compound >= 0.05:
    output = 'positive'
  elif (compound <= 0.05) and (compound >= -0.05):
    output = 'neutral'
  elif compound <= -0.05: 
    output = 'negative'
  print(output)
  print(image_to_text)
  return output
