# Test example: https://www.youtube.com/watch?v=BZP1rYjoBgI

from __future__ import unicode_literals
import youtube_dl
import sys

import mp3_tagger


# def my_hook(d):
#     if d['status'] == 'finished':
#         print('Done downloading, now converting ...')


# Download MP3 from Youtube
def downloadSong(link):

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        # 'noplaylist' : True,
	        'preferredquality': '192',
	        # 'progress_hooks': [my_hook],
	    }],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([linkYT])



lenArg = len(sys.argv)

mp3Retrived = ''

if lenArg >= 2:
	linkYT = sys.argv[1]
	mp3Retrive = downloadSong(linkYT)
else:
	print("No args provided")





if mp3Retrive != '':

	mp3 = MP3File("./SongTest.mp3")

	# Get default values
	oArtist = mp3.artist
	oAlbum 	= mp3.album
	oSong	= mp3.song
	oGenre	= mp3.genre


# mp3.set_version(VERSION_BOTH)




















