#!/usr/bin/env python3
import youtube_dl
import sys

from flask import Flask, Response, render_template
from flask import send_file
from jinja2 import Template



app = Flask(__name__)



@app.route('/')
def mainland():

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

	# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	# 	ydl.download(['https://www.youtube.com/watch?v=5ytzbr4SiKE'])

	template = []

	return render_template('index.html', test1 = template)


	#send_file('./helloWorld.mp3', as_attachment=True)




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
	app.run(debug=True,host='127.0.0.1',port=5001)














