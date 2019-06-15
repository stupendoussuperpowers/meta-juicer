# meta-juicer
writes song's correct metadata to its mp3 file

## Requirements
1) <a href = "https://github.com/beetbox/pyacoustid">pyacoustid</a> - python wrapper for AcoustID API
2) <a href="https://github.com/quodlibet/mutagen">mutagen</a> - python library to handle audio metadata
3) <a href="https://acoustid.org/chromaprint">Chromaprint</a> - required to work with pyacoustid
4) You will also need developer API key for <a href="https://acoustid.org/login">AcoustID</a> to access the fingerprint database and from <a href="https://www.last.fm/api/account/create">Last.fm</a> for metadata database

## Usage
1)Put the main python script and Chromaprint excecutable(fpcalc.exe) in the folder with all the music files you want to have metadata corrected
2)Run the script and that's it

## Todo
- add comments
- clean code
- better error handling
