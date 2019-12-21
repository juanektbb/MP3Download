#!/usr/bin/env python3
import youtube_dl
import sys, datetime, time, random

# https://pypi.org/project/tinytag/
# https://eyed3.readthedocs.io/en/latest/

from urllib import request, parse 
from urllib.parse import parse_qs

import eyed3
from tinytag import TinyTag


from flask import Flask, Response, render_template, request
from flask import send_file
from jinja2 import Template



app = Flask(__name__)


@app.route('/')
def mainland():

	fileName = getRandomString() + ".mp3"

	# Settings for downloading
	ydl_opts = {
		'forcetitle': True,
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	    'noplaylist' : True,
	    'progress_hooks': [my_hook],
	    'outtmpl': './' + fileName
	}

	# Download from youtube
	# youtube_dl.YoutubeDL(ydl_opts).download(['https://www.youtube.com/watch?v=5ytzbr4SiKE'])


	# USE TINY TAG TO GET ATTRIBUTES
	# fileTags = TinyTag.get(fileName)
	# print('This track is by %s.' % fileTags.artist)

	return Response("hello yeahss")
	#return render_template('index.html', fileName = fileName)

	#send_file('./helloWorld.mp3', as_attachment=True)





@app.route("/tags", methods=['POST','GET'])
def tags():

	fileName = request.form.get('fileName')

	songTitle = request.form.get('songTitle')
	songTitle = songTitle.capitalize()

	songArtist = request.form.get('songArtist')
	songArtist = upperArtist(songTitle)

	songGenre = request.form.get('songGenre')
	songAlbum = "Musica JD"

	# LOAD THIS FILE
	audio = eyed3.load(fileName)

	audio.initTag()

	

	audio.tag.title = unicode(songTitle)
	audio.tag.artist = unicode(songArtist)
	audio.tag.album_artist = unicode(songArtist)

	# audio.tag.genre = u"ccc"
	audio.tag.album = unicode(songAlbum)
	audio.tag.track = u""

	audio.tag.images.set(3, open('music.png','rb').read(), 'image/png')
	audio.tag.save()


	return Response(songGenre)






def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')



# RETURN ARTIST AS NICE STRING
def upperArtist(string):
	newList = list(string.split(" "))
	newString = ""

	for i in newList:
		if((i == "ft") or (i == "ft.")):
			newString += i + " "
		else:
			newString += i.capitalize() + " "

	return newString.strip()


# RETURN RANDOM STRING
def getRandomString():
	abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	retString = ""

	now = str(time.time()).split(".")

	for i in range(2):
		rand = random.randrange(0, len(abc))
		retString += abc[rand]

	retString += now[0]
	return retString






""" ***********************************
	FUNCTIONS FOR VIDEO INFORMATION
*********************************** """
# RETURN VIDEO ID
def returnVideoID(video):
	# Request video info and parse it 
	parsed = parse.urlparse(video)
	video_id = parse_qs(parsed.query)['v'][0]
	return video_id


# RETURN VIDEO TITLE
def returnVideoTitle(video):
	# Request video and scrape data
	resp = request.urlopen(video)
	data = resp.read()
	decode_data = data.decode("UTF-8")
	
	# Substring what is found between title tags
	video_title = decode_data.split("</title>")[0].split("<title>")[1].split(" - YouTube")[0]
	return video_title







if __name__ == '__main__':
	app.run(debug=True,host='127.0.0.1',port=5000)














