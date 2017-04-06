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


#Lastfm API stuff
API_KEY = "5745d2f8981f5dbe6ae366f7a7bb5534"
API_SECRET = "55134862cd12af09c7c8b6a9c77d16fa"
username = "deseaux"
password_hash = pylast.md5("EughhPassword?2")
 
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)
 
 
user = "selib" #input("User:")
days = 30 #input("Days looking back:")
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
 
 
import time
 
start = time.time()
print("starting")
 
listened_tracks = get_tracks(user,days)
 
artist_list = {}
album_list = {}


print("done fetching recent tracks")
 
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
 

print("done checking for duration")
 
if "None" in album_list:
    del album_list["None"]

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



draw(top9,user,album_list,network)
print("Draw done")
 
#list_artists = sorted(artist_list.items(), key=lambda x: x[1]) #Sorts the dict into a list
 

f = open('list.txt', 'w',encoding='utf-8')

if arOrAl == "ar":
    print("Listened artists:")
    for x in sorted(artist_list.items(), key=lambda x: x[1], reverse=True):
        name, value = x
        f.write('{}: {} Min'.format(name, int(value/60))) 
        f.write('\n')
  
elif arOrAl == "al":
    print("Listened albums:")
    for x in sorted(album_list.items(), key=lambda x: x[1], reverse=True):
        name, value = x
        f.write('{}: {} Min'.format(name, int(value[0]/60))) 
        f.write('\n')
  




end = time.time()
time_elapsed = end - start
print("Time elapsed: %fs" % time_elapsed)