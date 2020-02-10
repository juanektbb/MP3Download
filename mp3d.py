#!/usr/bin/env python3
import datetime, time, random, os, sys, json

import urllib.request 
from urllib import request, parse 
from urllib.parse import parse_qs, urlparse

import eyed3
import youtube_dl

from flask import Flask, Response, render_template, request as requestflask, send_file, jsonify
from jinja2 import Template

from pydub import AudioSegment 
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TT2
from mutagen.easyid3 import EasyID3

import pymongo 

# https://chodounsky.net/2019/03/24/progressive-web-application-as-a-share-option-in-android/

################### VARIABLES ###################

app = Flask(__name__)
routing = "./downloads/"

# DATABASE CONNECTION
mymongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mymongodb = mymongoclient["mp3d"]

# Mongo collections
mycollLand = mymongodb["land"]
mycollVideo = mymongodb["video"]
mycollDownloads = mymongodb["download"]

# My API token + URL
basicAPIurl = "https://geo.ipify.org/api/v1?apiKey=at_L0Wh0Mqx7E3TNIf3iVRgegZVesj0P&ipAddress="


#################### ROUTES ####################

"""'''''''''''''''''''''''''
		MAIN LANDING		
'''''''''''''''''''''''''"""
@app.route('/')
def mainland():
	insertToDB(requestflask, "land", None)
	return render_template("land.html");


# SUPPORTIVE ROUTE TO GET SERVICE WORKER
@app.route('/sw.js', methods=['GET'])
def serviceworker():
    return app.send_static_file('service-worker.js')


"""'''''''''''''''''''''''''''''
		MAIN VIDEO PAGE
'''''''''''''''''''''''''''''"""
@app.route('/video', methods=['POST'])
#@app.route('/video')
def videoland():

	possibleLinks = [
		'youtu.be',
		'www.youtu.be',
		'youtube.com',
		'www.youtube.com'
	]

	video_url = ""
	title_pwa = ""

	# Get data from the user
	if requestflask.method == "POST":
		video_url = requestflask.form.get("text")
		title_pwa = requestflask.form.get("title")

	# Testing
	# video_url = "https://www.youtube.com/watch?v=EzKImzjwGyM"
	# title_pwa = "This is a test video"

	# Render not found URL
	if video_url == "":
		return Response("<p style='text-align: center'>URL NOT FOUND <br><br> If error persist, contact the developer</p>")

	else:

		acceptableLink = False

		# If link belongs to Youtube
		query = urlparse(video_url)
		if query.hostname in possibleLinks:
			acceptableLink = True

		# Render not acceptable URL
		if not acceptableLink:
			return Response("<p style='text-align: center'>URL NOT VALID <br><br> " + video_url +" <br> If error persist, contact the developer</p>")
		
		video_id = returnVideoID(video_url)
		video_title = returnVideoTitle(video_url)

		fileName = getRandomString()

		insertToDB(requestflask, "video", video_url)
		return render_template('index.html', 
			fileName = fileName,
			videoUrl = video_url,
			videoId = video_id,
			videoTitle = video_title
		)


"""'''''''''''''''''''''''''''''''''''''
		ENDPOINT FOR DOWNLOADING
'''''''''''''''''''''''''''''''''''''"""
@app.route("/download", methods=['POST','GET'])
def download():

	fileName = requestflask.form.get('fileName')
	videoId = requestflask.form.get('videoId')
	videoUrl = requestflask.form.get('videoUrl')

	songTitle = requestflask.form.get('songTitle')
	songTitle = songTitle.capitalize()

	songArtist = requestflask.form.get('songArtist')
	songArtist = upperArtist(songArtist)

	songGenre = requestflask.form.get('songGenre')
	songIcon = requestflask.form.get('songIcon')
	songAlbum = "MP3D"


	# IF ICON IS FROM YOUTUBE
	if songIcon == "icon-yt":

		# Try to get icon
		try:
			theimage = 'https://img.youtube.com/vi/' + videoId + '/0.jpg'
			urllib.request.urlretrieve(theimage, routing + fileName + '.jpg')
		
		except IOError as e:
			return Response("<p style='text-align: center'>UNABLE TO DOWNLOAD YOUTUBE ICON <br><br> If error persist, contact the developer</p>")


	# TRY TO DOWNLOAD THE M4A FROM YOUTUBE
	try:

		# Settings for downloading
		ydl_opts = {
			'forcetitle': True,
			'verbose': True,
		    'format': 'bestaudio/best',
		    'ffmpeg_location': '/usr/bin/ffmpeg',
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'm4a',
		        'preferredquality': '192',
		    }],
		    'noplaylist' : True,
		    'outtmpl': routing + fileName + ".mp3"
		}
		  
		# Download from Youtube
		youtube_dl.YoutubeDL(ydl_opts).download([videoUrl])

	except IOError as a:
		return Response("<p style='text-align: center'>UNABLE TO DOWNLOAD MP3 <br><br> If error persist, contact the developer</p>")


	# LOAD THIS FILE TO MODIFY
	try:

		# CONVERT TO FILE MP3
		rawsongname = songTitle + ".mp3"
		mp3name = routing + rawsongname
		oldname = routing + fileName + ".m4a"
		wav_audio = AudioSegment.from_file(oldname, format="m4a")
		wav_audio.export(mp3name, format="mp3")

		# Remove the old M4A file
		os.remove(oldname)


		# OPEN THE IMAGE TO READ THE DATA
		if songIcon == "icon-yt":
			imageDownloaded = routing + fileName + '.jpg'
		else:
			imageDownloaded = './static/images/icon-mp3d.png'

		imagedata = open(imageDownloaded, 'rb').read()


		# SET ICON/IMAGE FOR THIS SONG
		id3 = ID3(mp3name)
		id3.add(APIC(3, 'image/jpg', 3, 'Front cover', imagedata))
		id3.add(TT2(encoding = 3, text = 'title'))
		id3.save(v2_version = 3)


		# SET ALL THE TAGS FOR THIS FILE
		audio = EasyID3(mp3name)
		audio["title"] = songTitle
		audio["artist"] = songArtist
		audio["albumartist"] = songArtist
		audio["genre"] = songGenre
		audio["album"] = songAlbum

		# audio["discnumber"] = u""
		# audio["date"] = u""
		# audio["originaldate"] = u""
		# audio["tracknumber"] = u""
		audio.save()


		# REMOVE ICON FROM YOUTUBE
		if songIcon == "icon-yt":
			os.remove(imageDownloaded)


		# RETURN THE FILE TO DOWNLOAD
		insertToDB(requestflask, "download", videoUrl)
		# return send_file(filename, as_attachment=True)
		return json.loads('{ "response":"success", "file":"' + rawsongname +  '" }');
		

	except IOError as a:
		return Response("<p style='text-align: center'>UNABLE TO CONVERT TO MP3 <br><br> If error persist, contact the developer</p>")


"""''''''''''''''''''''''''''''''''''''
	ENDPOINT TO TRIGGER DOWNLOADING
''''''''''''''''''''''''''''''''''''"""
@app.route("/trigger", methods=['GET','POST'])
def trigger():
	filename = requestflask.form.get('superInput')
	return send_file(routing + filename, as_attachment=True)


"""''''''''''''''''''''''''''''''''''''
		ENDPOINT TO DELETE FILE
''''''''''''''''''''''''''''''''''''"""
@app.route("/delete", methods=['GET','POST'])
def delete():
	filename = requestflask.form.get('superInput')
	# os.remove(routing + filename)
	return json.loads('{"response":"success"}');


################### FUNCTIONS ###################

""" **********************************
		FUNCTIONS FOR DATABASE
********************************** """
# INSERT INTO MONGO
def insertToDB(req, types, url):

	builtUrlAPI = basicAPIurl + req.remote_addr
	builtJSON = request.urlopen(builtUrlAPI)
	builtText = json.loads(builtJSON.read())

	mp3drecord = { 
		"type": types,
		"ip": req.remote_addr, 
		"country": builtText['location']['country'],
		"region": builtText['location']['region'],
		"city": builtText['location']['city'],
		"url": url,
		"created":  datetime.datetime.now() 
	}	

	if types == "land":
		mycollLand.insert_one(mp3drecord)
	elif types == "video":
		mycollVideo.insert_one(mp3drecord)
	elif types == "download":
		mycollDownloads.insert_one(mp3drecord)


""" *********************************
		FUNCTIONS FOR STRINGS
********************************* """
# RETURN ARTIST AS NICE STRING
def upperArtist(string):
	string = string.lower()
	newList = list(string.split(" "))
	newString = ""

	for i in newList:
		if((i == "ft") or (i == "ft.")):
			newString += "ft. "
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

	query = urlparse(video)
	if query.hostname in ('youtu.be', 'www.youtu.be'):
	    return query.path[1:]

	if query.hostname in ('www.youtube.com', 'youtube.com'):
		
	    if query.path == '/watch':
	        p = parse_qs(query.query)
	        return p['v'][0]

	    if query.path[:7] == '/embed/':
	        return query.path.split('/')[2]

	    if query.path[:3] == '/v/':
	        return query.path.split('/')[2]

	return None


# RETURN VIDEO TITLE
def returnVideoTitle(video):

	# Request video and scrape data
	resp = request.urlopen(video)
	data = resp.read()
	decode_data = data.decode("UTF-8")
	
	# Substring what is found between title tags
	video_title = decode_data.split("</title>")[0].split("<title>")[1].split(" - YouTube")[0]
	return video_title


################## APPLICATION ##################
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)