# Undefined Genre Tag Finder
<br/>
From the root directory of the script recursively scans the genre tag of specified audio file types and compares it with a given list of known genres.
The files with unidentified genres are displayed on the console.
All concerned files are printed into a m3u8 file for easy dragging into OneTagger or Mp3Tag.
All unidentified genres are printed into a txt file alphabetically.

(Only tested on Windows 10)

#### Supported file types
- aif(f)
- flac
- AAC (m4a)
- mp3
- ogg
- wav

## Requirements
- Python 3.11 or higher
- [mutagen](https://pypi.org/project/mutagen/)
- [colorama](https://pypi.org/project/colorama/)

## Installation
- Download Source
- Install Requirements <br/>```pip install -r requirements.txt```

## Usage
1. Put ```find_undefined_genres.py``` in the root folder of the folder structure you want to scan.
2. Open ```find_undefined_genres.py``` in a text editor.
3. Navigate to line 12, add/remove the desired file types you want to scan, and save the changes.
4. Navigate to line 15, list all the genres you want to exclude in the search between the two single quotes, separate them by comma, and save the changes. <br/> Example: ```'Deep House, Techo, Drum & Bass'```
5. Then execute the script with the command ```python find_undefined_genres.py```.