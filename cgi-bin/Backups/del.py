from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import pylast
import urllib.request
import os.path
import os
import sys

"""
API_KEY = "5745d2f8981f5dbe6ae366f7a7bb5534"
API_SECRET = "55134862cd12af09c7c8b6a9c77d16fa"
username = "deseaux"
password_hash = pylast.md5("EughhPassword?2")
 
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
    API_SECRET, username = username, password_hash = password_hash)
 
user = 'selib'
time_period = 'Top Albums (Last 7 Days)'

albums = network.get_user(user).get_top_albums(period=pylast.PERIOD_7DAYS, limit=9) 
"""
fu = open('list1.txt', 'w',encoding='utf-8') 

fu.write("done checking for duration")
for root, dirs, filenames in os.walk("images/"):
#filelist = [ f for f in os.listdir("images/") if f.endswith(".png") ]
	for filename in filenames:
		filename = os.path.join(root, filename)
		fu.write(filename+"\n")
		os.remove(filename)
		
print("done")	


#draw()