import eyed3
from tinytag import TinyTag

audio = eyed3.load("./GC1576618455.mp3")

# if(audio.tag == None):
# 	audio.initTag()

# audio.tag.images.set(3, open('music.png','rb').read(), 'image/png')

# audio.tag.title = u"aaa"
# audio.tag.artist = u"bb"
# audio.tag.album_artist = u"bb"

# # audio.tag.genre = u"ccc"
# audio.tag.album = u"Musica JD"
# audio.tag.track = u"dd"

# audio.tag.save()

# # USE TINY TAG TO GET ATTRIBUTES
# tag = TinyTag.get('./GC1576618455.mp3')
# print('Title %s.' % tag.title)
# print('Artist %s.' % tag.artist)
# print('Album Artist %s.' % tag.albumartist)
# print('Genre %s.' % tag.genre)
# print('Album %s.' % tag.album)
# # Image

# print('Disc %s.' % tag.disc)
# print('Year %s.' % tag.year)
# print('Track %s.' % tag.track)
# print('Comment %s.' % tag.comment)


thisString = "Hello ft. world, yeah"
newList = list(thisString.split(" "))
newString = ""

for i in newList:
	if((i == "ft") or (i == "ft.")):
		newString += i + " "
	else:
		newString += i.capitalize() + " "

newString = newString.strip()

print(newString)