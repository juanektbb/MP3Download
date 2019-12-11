import mp3_tagger
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH






# if mp3Retrive != '':


# MAKE IF FILE EXISTS


mp3 = MP3File("./Paris.mp3")

# Get default values

print(mp3.get_tags())
