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
     ''
     .replace('\r', '').replace('\n', '').split(',')]
)


def get_project_root() -> Path:
    return Path(__file__).parent


def check_filetype(files, filetype) -> tuple:
    result = []
    undefined_genres_summary_per_type = []

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
            return result, undefined_genres_summary_per_type

    for relative_filepath in files:
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
                    undefined_genres_summary_per_type.extend(undefined_genres)

        except Exception as e:
            print(f'{str(e)}\n')

    return result, undefined_genres_summary_per_type


if __name__ == '__main__':
    just_fix_windows_console()
    root_path = str(get_project_root())
    m3u8 = []
    undefined_genres_summary = set()

    for filetype in FILETYPES:
        print(f'\033[96mNow Checking {filetype} files.\033[0m')
        files = glob.glob(f'**/*.{filetype}', recursive=True)
        m3, undef = check_filetype(files, filetype)
        m3u8.extend(m3)
        undefined_genres_summary.update(undef)

    if len(m3u8) > 0:
        m3u8.sort()
        with open('results.m3u8', 'w', encoding="utf-8") as results:
            results.write('\n'.join(m3u8))

    if len(undefined_genres_summary) > 0:
        undefined_genres_summary = sorted(undefined_genres_summary)
        output = '\n'.join(undefined_genres_summary)
        print(f'\033[4mUndefined genres summary:\033[0m\n\033[1;33m{output}\033[0m')
        with open('results.txt', 'w', encoding="utf-16") as results:
            results.write(output)

