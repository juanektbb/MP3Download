#!/usr/bin/env python3
import youtube_dl
import sys

from flask import Flask, Response
from flask import send_file
app = Flask(__name__)



@app.route('/')
def hello_world():

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
	    'outtmpl': './helloWorld.mp3'
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download(['https://www.youtube.com/watch?v=5ytzbr4SiKE'])


	return send_file('./helloWorld.mp3', as_attachment=True)




def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


# #Download MP3 from Youtube
# def downloadSong(link):




lenArg = len(sys.argv)

mp3Retrived = ''

if lenArg >= 2:
	linkYT = sys.argv[1]
	#mp3Retrive = downloadSong(linkYT)
else:
	print("No URL provided")





if __name__ == '__main__':
    app.run()













