#!/usr/bin/env python3
import cgi
from queue import Queue
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from P import draw
import pylast
import datetime
import time
import threading
import urllib
import os.path
import os
import sys

form = cgi.FieldStorage()                 # parse form data


print('Content-type: text/html\n')        # hdr plus blank line
print('<title>Reply Page</title>')        # html reply page
if not 'dank' in form:
    print('<h1>Who are you?</h1>')
else:
    print('<h1>Hello <i>%s</i>!</h1>' % cgi.escape(form['dank'].value))



#Lastfm API stuff
API_KEY = "5745d2f8981f5dbe6ae366f7a7bb5534"
API_SECRET = "55134862cd12af09c7c8b6a9c77d16fa"
username = "deseaux"
password_hash = pylast.md5("EughhPassword?2")
 
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)
 
 
user = cgi.escape(form['dank'].value) #input("User:")
days = int(cgi.escape(form['tme'].value)) #input("Days looking back:")
arOrAl = "al" #input("Display album or artist:")

def get_tracks(user,days): #returns a list of the tracks the user has listened to
    lastfm_user = network.get_user(user)
 
    #network.enable_rate_limit()
 
    #Something about the current time
    diff = datetime.date.today() - datetime.timedelta(int(days))
    s = diff.strftime("%d/%m/%Y")
    unix = int(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))
 
    diff2 = datetime.date.today() - datetime.timedelta(int(343))
    s2 = diff2.strftime("%d/%m/%Y")
    unix2 = int(time.mktime(datetime.datetime.strptime(s2, "%d/%m/%Y").timetuple()))
 


    #actually gets the recently listened tracks
    tracklist = lastfm_user.get_recent_tracks(limit=None,time_from=unix) #,time_to=unix2
    return tracklist
 
f = open('list.txt', 'w',encoding='utf-8') 
import time
 
start = time.time()

 
listened_tracks = get_tracks(user,days)

nl=[]

for x in listened_tracks:
	nl.append(x[0])


my_dict = {i:nl.count(i) for i in nl}

for key, value in my_dict.items() :
    f.write(str(key)+str(value)+"\n")



artist_list = {}
album_list = {}




f.write("done fetching recent tracks")
 
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
 
threads = [threading.Thread(target=check_duration, args=(trk,)) for trk in listened_tracks]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
 
fu = open('list3.txt', 'w',encoding='utf-8') 

fu.write("done checking for duration")
 
if "None" in album_list:
    del album_list["None"]
if "None" in artist_list:
    del artist_list["None"]
	
	
top9 = []
countTo9 = 0
if arOrAl == "al":
    for x in sorted(album_list.items(), key=lambda x: x[1], reverse=True):
        name, value = x
        y = network.get_album(value[1],name)
        top9.append(y)
        countTo9+=1
        if countTo9 > 8:
            break
elif arOrAl == "ar":
    for x in sorted(artist_list.items(), key=lambda x: x[1], reverse=True):
        name, value = x
        y = network.get_artist(name)
        top9.append(y)
        countTo9+=1
        if countTo9 > 8:
            break



if arOrAl == "al":
	draw(top9,user,album_list,network,arOrAl)
if arOrAl == "ar":
	draw(top9,user,artist_list,network,arOrAl)
	
fu.write("Draw done")
 
#list_artists = sorted(artist_list.items(), key=lambda x: x[1]) #Sorts the dict into a list
 


fu.write("u open done")

print("<img src=\"../output/{}.png\" width=900 height=900 border=0 alt=\"\"> <br>".format(cgi.escape(form['dank'].value)))

fu.write("print image done")	

if arOrAl == "al":
    print("Listened albums:")
    for x in sorted(album_list.items(), key=lambda x: x[1], reverse=True):
        name, value = x
        print('{}: {} Min'.format(name, int(value[0]/60))) 
        print('<br>')
  	
if arOrAl == "ar":
    print("Listened artists:")
    for x in sorted(artist_list.items(), key=lambda x: x[1], reverse=True):
        name, value = x
        print('{}: {} Min'.format(name, int(value/60))) 
        print('<br>')
  	


	
fu.write("print html done")


end = time.time()
time_elapsed = end - start


fu.write("end time down done")	
print("Time elapsed: %fs" % time_elapsed)
fu.write("end of doc")	
fu.close()