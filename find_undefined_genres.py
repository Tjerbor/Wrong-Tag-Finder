import glob
from pathlib import Path

from colorama import just_fix_windows_console
from mutagen.aiff import AIFF
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE

FILETYPES = sorted({'aif', 'aiff', 'flac', 'm4a', 'mp3', 'ogg', 'wav'})
GENRES = set(
    [genre.strip() for genre in
     'Future House, Modern House, Dubstep, House, Progressive, Colour House'
     .replace('\r', '').replace('\n', '').split(',')]
)


def get_project_root() -> Path:
    return Path(__file__).parent


def check_filetype(files) -> list:
    result = []

    for relative_filepath in files:
        match filetype:
            case ftype if ftype in ['aif', 'aiff']:
                mutagen_type = AIFF
                genre_fieldname = 'TCON'
            case 'flac':
                mutagen_type = FLAC
                genre_fieldname = 'genre'
            case 'm4a':
                mutagen_type = MP4
                genre_fieldname = '©gen'
            case 'mp3':
                mutagen_type = EasyID3
                genre_fieldname = 'genre'
            case 'ogg':
                mutagen_type = OggVorbis
                genre_fieldname = 'genre'
            case 'wav':
                mutagen_type = WAVE
                genre_fieldname = 'TCON'
            case _:
                print(f'\033[93mUndefined filetype \"{filetype}\"\033[0m\n')
                return result

        try:
            audio = mutagen_type(relative_filepath)

            if genre_fieldname in audio.keys():
                genre_fields = audio[genre_fieldname]

                # join duplicate fields (Will not work with m4a files)
                genrestring = ','.join(genre_fields)

                # split genres
                genres = [genre.strip() for genre in genrestring.split(',')]

                undefined_genres = list(set(genres) - GENRES)

                if len(undefined_genres) != 0:
                    print(relative_filepath)
                    print(f'Undefined Genres:{undefined_genres}\n')
                    result.append(root_path + '\\' + relative_filepath)

        except Exception as e:
            print(f'{str(e)}\n')

    return result


if __name__ == '__main__':
    just_fix_windows_console()
    root_path = str(get_project_root())
    m3u8 = []

    for filetype in FILETYPES:
        print(f'\033[96mNow Checking {filetype} files.\033[0m')
        files = glob.glob(f'**/*.{filetype}', recursive=True)
        m3u8.extend(check_filetype(files))

    if len(m3u8) > 0:
        m3u8.sort()
        with open('results.m3u8', 'w') as results:
            results.write('\n'.join(m3u8))
