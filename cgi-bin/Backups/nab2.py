#!/usr/bin/env python3
import cgi
import pylast
import datetime
import time
import threading
import urllib
import os.path
import os
import sys

form = cgi.FieldStorage()                 # parse form data


diff = datetime.date.today() - datetime.timedelta(int(-1))
s = diff.strftime("%d/%m/%Y")
unix = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))

#Lastfm API stuff
API_KEY = "5745d2f8981f5dbe6ae366f7a7bb5534"
API_SECRET = "55134862cd12af09c7c8b6a9c77d16fa"
username = "selib"
password_hash = pylast.md5("swordofseals")
 
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)
 
 
network.scrobble("Youre shit alex","stfu",time.time())
 
 
y=input("sd")
 
 