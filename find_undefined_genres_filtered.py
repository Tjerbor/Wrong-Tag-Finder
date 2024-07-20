import glob

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE

FILETYPES = set(['flac', 'm4a', 'mp3', 'ogg', 'wav'])
GENRES = set(
    [genre.strip() for genre in
     'BPMCHANGE,Omnigenre,Acid House,Disco House,French House,Ghetto House,Jackin House,Melodic House,OS Future House,Progressive House,Soulful House,Speed House,'
     ' Complextro,Disco,Electro Swing,Future Bounce,Future Funk,Hardcore,Hardstyle,Hoe Trappin,Jall,Jersey Club,Meme,Pop,Psytrance,Riddim,Tearout,Techno,Trance,Trap,Chillwave,Synthwave,'
     'Bass House,Colour House,Deep House ,Future House,Modern House,Piano House,Lofi House,Tech House,Colour Bass,Dubstep ,Breakcore,DnBnB'
     'Liquid DnB,Melodic DnB,Garage, Normie, Techcore'
     .split(',')]
)
GROUPING = 'For Mixing'


def check_filetype(files):
    global curse_height
    for filepath in files:
        grouping_field_exists_and_corrects = False

        match filetype:

            case 'flac':
                audio = FLAC(filepath)
                genre_fieldname = 'genre'
                grouping_key_name = 'grouping'
                grouping_tag_fieldname = 'GROUPING'

                if (grouping_key_name in audio.keys()):
                    grouping_refined = str(audio[grouping_tag_fieldname][0])
                    if (grouping_refined == GROUPING):
                        grouping_field_exists_and_corrects = True
            case 'm4a':
                audio = MP4(filepath)
                genre_fieldname = '©gen'
                grouping_fieldname = '----:com.apple.iTunes:GROUPING'
                if (grouping_fieldname in audio.keys()):
                    grouping_raw = str(audio['----:com.apple.iTunes:GROUPING'][0])
                    grouping_refined = grouping_raw[2:len(grouping_raw) - 1]

                    if (grouping_refined == GROUPING):
                        grouping_field_exists_and_corrects = True
            case 'mp3':
                audio = EasyID3(filepath)
                genre_fieldname = 'genre'
                grouping_fieldname = 'GRP1'
                helper = ID3(filepath)
                if (grouping_fieldname in helper.keys() and helper[grouping_fieldname] == GROUPING):
                    grouping_field_exists_and_corrects = True
            case 'ogg':
                audio = OggVorbis(filepath)
                genre_fieldname = 'genre'
                grouping_fieldname = 'grouping'
                if (grouping_fieldname in audio.keys()):
                    grouping_refined = str(audio[grouping_fieldname][0])
                    if (grouping_refined == GROUPING):
                        grouping_field_exists_and_corrects = True
            case 'wav':
                audio = WAVE(filepath)
                genre_fieldname = 'TCON'
                grouping_fieldname = 'GRP1'
                if (grouping_fieldname in audio.keys() and audio[grouping_fieldname] == GROUPING):
                    grouping_field_exists_and_corrects = True
            case _:
                print(f'\033[93mUndefined filetype \"{filetype}\"\033[0m\n')
                return

        if (genre_fieldname in audio.keys() and grouping_field_exists_and_corrects):
            genre_fields = audio[genre_fieldname]

            # join duplicate fields (Will not work with m4a files)
            genrestring = ','.join(genre_fields)

            # split genres
            genres = [genre.strip() for genre in genrestring.split(',')]

            undefined_genres = list(set(genres) - GENRES)

            if (len(undefined_genres) != 0):
                print(filepath)
                print(f'Undefined Genres:{undefined_genres}\n')


if __name__ == '__main__':

    for filetype in FILETYPES:
        print (f'Now Checking {filetype} files.')
        files = glob.glob(f'**/*.{filetype}', recursive=True)
        check_filetype(files)
