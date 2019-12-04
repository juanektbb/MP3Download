from __future__ import unicode_literals
import youtube_dl
import sys


linkYT = sys.argv[1];


if linkYT != null: 

	ydl_opts = {
	    'format': 'bestaudio/best',
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	    ydl.download([linkYT])


else:
	print("No args provided")






