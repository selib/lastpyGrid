#!/usr/bin/env python3
import cgi
from queue import Queue
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from P import draw
import concurrent.futures 
import pylast
import datetime
import time
import threading
import urllib
import os.path
import os
import sys

form = cgi.FieldStorage()				  # parse form data

#Lastfm API stuff
API_KEY = "5745d2f8981f5dbe6ae366f7a7bb5534"
API_SECRET = "55134862cd12af09c7c8b6a9c77d16fa"

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
 
 

print('Content-type: text/html\n')		  # hdr plus blank line
print('<title>Reply Page</title>')		  # html reply page

if not 'usr' in form:
	print('<h1>Who are you?</h1>')
else:
	user = cgi.escape(form['usr'].value)
	print('<h1>Hello <i>%s</i>!</h1>' % user) 
	
if not 'tme' in form:
	days = 1
else:
	days = int(cgi.escape(form['tme'].value)) 
	
if not 'aroral' in form:
	arOrAl = "al"
else:
	arOrAl = cgi.escape(form["aroral"].value)
	
if not 'timeto' in form:
	timeto = None
else:
	timeto = int(cgi.escape(form["timeto"].value))
				
def get_tracks(user,days): #returns a list of the tracks the user has listened to
	lastfm_user = network.get_user(user)
 
	#Something about the current time
	diff = datetime.date.today() - datetime.timedelta(int(days))
	s = diff.strftime("%d/%m/%Y")
	unix = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
 
	if(timeto != None):
		diff2 = datetime.date.today() - datetime.timedelta(int(timeto))
		s2 = diff2.strftime("%d/%m/%Y")
		unix2 = int(time.mktime(datetime.datetime.strptime(s2, "%d/%m/%Y").timetuple()))
	else:
		unix2 = None

	#actually gets the recently listened tracks
	tracklist = lastfm_user.get_recent_tracks(limit=None,time_from=unix,time_to=unix2,cacheable=True) #,time_to=unix2
	return tracklist

 
start = time.time()

listened_tracks = get_tracks(user,days)

artist_list = {}
album_list = {}

if arOrAl == "ar":
	list_in_use = artist_list
elif arOrAl == "al":
	list_in_use = album_list
 
lock = threading.Lock()
def check_duration(track):
	global lock
	artist_name = str(track[0].artist)
	album_name = str(track[1])
	if arOrAl == "ar":
		if artist_name not in artist_list: #Check if the artist is already in the dict
			artist_list[artist_name] = 0
	elif arOrAl == "al":
		if album_name not in album_list: #Check if the artist is already in the dict
			album_list[album_name] = [0,artist_name]
	else:
		return
	try:
		duration = track[0].get_duration()
		lock.acquire()
		if arOrAl == "ar":
			artist_list[str(track[0].artist)]+=duration/1000
		elif arOrAl == "al":
			album_list[str(track[1])][0]+=duration/1000 #if the artist is already on there just add the current track length
	except:
		pass
	finally:
		lock.release()

#Executes the check_duration function for each track in the listened_track list as a thread.		
with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
	future_to_url = {executor.submit(check_duration, trk): trk for trk in listened_tracks}
	for future in concurrent.futures.as_completed(future_to_url):
		trk = future_to_url[future]
 
 
if "None" in list_in_use:
	del list_in_use["None"]
	
top9 = []
countTo9 = 0
for x in sorted(list_in_use.items(), key=lambda x: x[1], reverse=True):
	name, value = x
	if arOrAl == "al":
		y = network.get_album(value[1],name)
	elif arOrAl == "ar":
		y = network.get_artist(name)
	top9.append(y)
	countTo9+=1
	if countTo9 > 8:
		break



draw(top9,user,list_in_use,network,arOrAl)

print("<img src=\"../output/{}.png\" width=900 height=900 border=0 alt=\"\"> <br>".format(cgi.escape(form['usr'].value)))

print("Listened:")

for x in sorted(list_in_use.items(), key=lambda x: x[1], reverse=True):
	name, value = x
	if arOrAl == "al":
		print('{}: {} Min'.format(name, int(value[0]/60))) 
	if arOrAl == "ar":
		print('{}: {} Min'.format(name, int(value/60))) 
	print('<br>')

end = time.time()
time_elapsed = end - start

print("Time elapsed: %fs" % time_elapsed)