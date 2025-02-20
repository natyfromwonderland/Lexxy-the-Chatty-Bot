#! /usr/bin/python3
from flask import Flask, render_template, request
import random
import csv
import os
import urllib.parse
from botConfig import myBotName, chatBG, botAvatar, useGoogle, confidenceLevel
from botRespond import getResponse
import requests
import json

##Experimental Date Time
from dateTime import getTime, getDate
from dateTime import getWeekday

application = Flask(__name__)

chatbotName = myBotName
print("Bot Name set to: " + chatbotName)
print("Background is " + chatBG)
print("Avatar is " + botAvatar)
print("Confidence level set to " + str(confidenceLevel))

#Create Log file
try:
    file = open('BotLog.csv', 'r')
except IOError:
    file = open('BotLog.csv', 'w')

def tryGoogle(myQuery):
    myQuery = myQuery.replace("'", "%27")
    showQuery = urllib.parse.unquote(myQuery)
    return "<br><br>You can try this from my friend Google: <a target='_blank' href='https://www.google.com/search?q=" + myQuery + "'>" + showQuery + "</a>"


def chuck():

    api_url = 'https://api.api-ninjas.com/v1/chucknorris'

    response = requests.get(
        api_url, headers={'X-Api-Key': '0KlBPuagJIt0ugFTCjgamg==6HJbSVLUWRvJjQQ1'})
    if response.status_code == requests.codes.ok:
       joke = json.loads(response.text)
       return joke['joke']
    else:
       print("Error:", response.status_code, response.text)


def happyReaction():
    return '<h2>&#128516;</h2>'

def sadReaction():
    return '<h2>&#128553;</h2>'

@application.route("/")
def home():
    return render_template("index.html", botName = chatbotName, chatBG = chatBG, botAvatar = botAvatar)

@application.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botReply = str(getResponse(userText))
    if botReply == "IDKresponse":
        botReply = str(getResponse('IDKnull')) ##Send the i don't know code back to the DB
        if useGoogle == "yes":
            botReply = botReply + tryGoogle(userText)
    elif botReply == "getTIME":
        botReply = getTime()
        print(getTime())
    elif botReply == "getDATE":
        botReply = getDate()
        print(getDate())
    elif botReply == "getWeekday":
        botReply = getWeekday()
        print(getWeekday())
    elif botReply == "getJoke":
        botReply = chuck()
        print(chuck())
    elif botReply == "getHappy":
        botReply = happyReaction()
    elif botReply == "getSad":
        botReply = sadReaction()
    ##Log to CSV file
    print("Logging to CSV file now")
    with open('BotLog.csv', 'a', newline='') as logFile:
        newFileWriter = csv.writer(logFile)
        newFileWriter.writerow([userText, botReply])
        logFile.close()
    return botReply


if __name__ == "__main__":
    #application.run()
    application.run(host='0.0.0.0', port=80)
