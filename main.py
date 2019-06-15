import acoustid
import urllib.request
import json
import os
from mutagen.easyid3 import EasyID3

#acoustid_key = '' #enter your acoustid api key here
#lastfm_key = '' #enter you lastfm api key here

class Error(Exception):
	pass
	
class IDError(Error):
	pass

def gen_fingerprint(filename):
	return acoustid.fingerprint_file(filename)
	
def match_fingerprint(fprnt, api_key):
	return acoustid.lookup(api_key, fprnt[1], fprnt[0])

def fetch_aid_data(fprnt_data):
	if fprnt_data['results']:
		try:
			detail_loc = fprnt_data['results'][0]['recordings'][0]
			artist, title = detail_loc['artists'][0]['name'] , detail_loc['title']
		except KeyError:
			raise IDError
			return
		return artist, title
	else:
		raise ValueError("no fingerprint in acoustid database")
	
def fetch_metadata(artist, title, api_key):
	artist = '%20'.join(artist.split())
	title = '%20'.join(title.split())
	url = ('http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=%s&artist=%s&track=%s&format=json' % (api_key, artist, title))
	#print(url)
	
	with urllib.request.urlopen(url) as response:
		contents = response.read()
	
	contents_decoded = json.loads(contents)
	return contents_decoded
	
def apply_metadata(data, filename):

	audio = EasyID3(filename)
	try:
		title = validate_save(data['track']['name'])
		audio['title'] = title
		artist = data['track']['artist']['name']
		audio['artist'] = artist
		audio['albumartist'] = artist
		album_title = data['track']['album']['title']
		audio['album'] = album_title
		genre = ''
		for i in range(len(data['track']['toptags']['tag'])):
			genre += ('%s;' % (data['track']['toptags']['tag'][i]['name']))
		audio['genre'] = genre
	except KeyError:
		raise IDError
		return
	audio.save()
	os.rename(filename, title + '.mp3')

def main_process(file, acoustid_key, lastfm_key):
	print("processing...", end="")
	try:
		arty, name = (fetch_aid_data(match_fingerprint(gen_fingerprint(file), acoustid_key)))
		mdata = (fetch_metadata(arty, name, lastfm_key))
		apply_metadata(mdata, file)
		print("done")
	except IDError:
		print("error(insufficient data in AcoustID database))")
	except ValueError:
		print("error(audio fingerprint not found in AcoustID)")


def validate_save(filename):
	invalids = ['<', '>', '?', '|', '/','\\',':','*','#',"'",'"']
	for i in invalids:
		    filename.replace(i, "")
	return filename

def main():
	acoustid_key = ''
	lastfm_key = ''
	if not acoustid_key:
		acoustid_key = input("Enter your AcoustID API key: ")
	if not lastfm_key:
		lastfm_key = input("Enter your Last.fm API key: ")
	path = os.getcwd()
	files = (os.listdir(path))
	for file in files:
		if file[-4::] == '.mp3':
			print(file, end="- ")
			main_process(file, acoustid_key, lastfm_key)
		else:
			continue

if __name__ == "__main__":
	main()
