#!/usr/bin/env python3
import sys, datetime, time, random, os

from urllib import request, parse 
from urllib.parse import parse_qs, urlparse

import eyed3
import youtube_dl

from flask import Flask, Response, render_template, request as requestflask, send_file
from jinja2 import Template

# https://pypi.org/project/tinytag/
# https://eyed3.readthedocs.io/en/latest/
# https://chodounsky.net/2019/03/24/progressive-web-application-as-a-share-option-in-android/

app = Flask(__name__)

# 
@app.route('/')
def mainland():
	return render_template("land.html");


# Supportive route to get Service Worker
@app.route('/sw.js', methods=['GET'])
def serviceworker():
    return app.send_static_file('service-worker.js')





@app.route('/video', methods=['POST'])
def videoland():

	possibleLinks = [
		'http://youtube.com',
		'http://www.youtube.com',
		'https://.youtube.com',
		'https://www.youtube.com',
		'http://youtu.be',
		'http://www.youtu.be',
		'https://youtu.be',
		'https://www.youtu.be',
	]

	video_url = ""
	title_pwa = ""

	if requestflask.method == "POST":
		video_url = requestflask.form.get("text")
		title_pwa = requestflask.form.get("title")


	if video_url == "":
		return render_template("index.html",
			error = "UrlNotFound")


	else:

		acceptableLink = False

		# Get the link provided by the user
		parsed_uri = urlparse(video_url)
		urireturned = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

		return Response(urireturned)

		# If link belongs to Youtube
		if urireturned in possibleLinks or urireturned[:-1] in possibleLinks:
			acceptableLink = True


		# If the link is not acceptable
		if not acceptableLink:

			return render_template("index.html",
				error = "UrlNotAcceptable",
				url = urireturned
			)



		video_id = returnVideoID(video_url)
		video_title = returnVideoTitle(video_url)



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
		    'outtmpl': './' + fileName
		}




		# Download from youtube
		# youtube_dl.YoutubeDL(ydl_opts).download(['https://www.youtube.com/watch?v=5ytzbr4SiKE'])

		return render_template('index.html', 
			fileName = fileName,
			videoUrl = video_url,
			videoId = video_id,
			videoTitle = video_title
		)


# ENDPOINT FOR DOWNLOADING
@app.route("/download", methods=['POST','GET'])
def download():

	fileName = requestflask.form.get('fileName')

	songTitle = requestflask.form.get('songTitle')
	songTitle = songTitle.capitalize()

	songArtist = requestflask.form.get('songArtist')
	songArtist = upperArtist(songTitle)

	songGenre = requestflask.form.get('songGenre')
	songAlbum = "Musica JD"

	# LOAD THIS FILE
	try:
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

		os.rename(fileName, songTitle+".mp3")

		send_file(songTitle+".mp3", as_attachment=True)

	except IOError:
		return Response("Wrong")














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

""" ******************************* """

# RUN FLASK APP
if __name__ == '__main__':
	app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))