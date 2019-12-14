#!/usr/bin/env python3
import youtube_dl
import sys
import datetime
import time

# https://pypi.org/project/tinytag/
# https://eyed3.readthedocs.io/en/latest/


from tinytag import TinyTag


from flask import Flask, Response, render_template, request
from flask import send_file
from jinja2 import Template

import random


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


	template = []
	return render_template('index.html', test1 = template)

	#send_file('./helloWorld.mp3', as_attachment=True)





@app.route("/tags", methods=['POST','GET'])
def tags():


	songTitle = request.form.get('songTitle')
	songTitle = songTitle.capitalize()


	print(username)

	return Response(username)






def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


# #Download MP3 from Youtube
# def downloadSong(link):


def upperArtist(string):
	



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










lenArg = len(sys.argv)

mp3Retrived = ''

if lenArg >= 2:
	linkYT = sys.argv[1]
	#mp3Retrive = downloadSong(linkYT)
else:
	print("No URL provided")




if __name__ == '__main__':
	app.run(debug=True,host='127.0.0.1',port=5002)














