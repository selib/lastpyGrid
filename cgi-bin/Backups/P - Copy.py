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

def draw(albums,user,album_list,network,arOrAl):

    file_names = []
    for album in albums:
        try:
        	album_image = album.get_cover_image(pylast.COVER_EXTRA_LARGE)
        except:
        	album_image = network.get_album("Prince","The Black Album").get_cover_image(pylast.COVER_EXTRA_LARGE)
        file_name = os.getcwd() + '/images/'
        file_name += album_image[album_image.rfind('/')+1:]
        if not os.path.isfile(file_name):
            image_file = urllib.request.FancyURLopener()
            image_file.retrieve(album_image, file_name)
        file_names.append([file_name, album.artist.name, album.title])

    grid_image = Image.new('RGB', (900, 900))
    font = ImageFont.truetype("fonts/Roboto-Medium.ttf", 32)
    small_font = ImageFont.truetype("fonts/SourceCodePro-Medium.ttf", 16)
    draw = ImageDraw.Draw(grid_image, 'RGBA')

    for i in range(0, 900, 300):
        for j in range(0, 900, 300):
            array_position = int(j/300*3 + i/300)
            artist_name = file_names[array_position][1]
            album_title = file_names[array_position][2]
            album_title = (album_title[:27] + '..') if len(album_title) > 27 else album_title
            artist_name = (artist_name[:27] + '..') if len(artist_name) > 27 else artist_name
            length = "{} Min".format(str(int(album_list[file_names[array_position][2]][0]/60)))

            image = Image.open(file_names[array_position][0])
            grid_image.paste(image, (i, j))

            # lmao making an outline for the text is dumb
            draw.text((i+2, j+2), artist_name, (0, 0, 0), font=small_font)
            draw.text((i+1, j+1), artist_name, (255, 255, 255), font=small_font)

            draw.text((i+2, j+21), album_title, (0, 0, 0), font=small_font)
            draw.text((i+1, j+20), album_title, (255, 255, 255), font=small_font)

            draw.text((i+2, j+40), length, (0, 0, 0), font=small_font)
            draw.text((i+1, j+39), length, (255, 255, 255), font=small_font)


    #draw.text((10, 5), user + ' - ' + time_period, (255, 255, 255), font=font)
    grid_image.save(os.getcwd() + '/output/' + user + '.png')
    for root, dirs, filenames in os.walk("images/"):
	    for filename in filenames:
		    filename = os.path.join(root, filename)
		    os.remove(filename)
		


#draw()