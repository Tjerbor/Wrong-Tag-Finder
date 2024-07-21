import glob
from pathlib import Path

from colorama import just_fix_windows_console
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE

FILETYPES = sorted({'flac', 'm4a', 'mp3', 'ogg', 'wav'})
GENRES = set(
    [genre.strip() for genre in
     'BPMCHANGE,Omnigenre,Acid House,Disco House,French House,Ghetto House,Jackin House,Melodic House,OS Future '
     'House,Progressive House,Soulful House,Speed House,Complextro,Disco,Electro Swing,Future Bounce,Future Funk,'
     'Hardcore,Hardstyle,Hoe Trappin,Jall,Jersey Club,Meme,Pop,Psytrance,Riddim,Tearout,Techno,Trance,Trap,Chillwave,'
     'Synthwave,Bass House,Colour House,Deep House ,Future House,Modern House,Piano House,Lofi House,Tech House,'
     'Colour Bass,Dubstep ,Breakcore,DnBnB,Liquid DnB,Melodic DnB,Garage, Normie, Techcore,Drumstep,Melodic Dubstep,'
     'Brazilian Bass,undef,Tribal House,City Pop,Cyberneuro, Neurobass,Anime,Electro,Nightcore,Multigenre,'
     'Colour Trance,Colour DnBnB,Hi-TECH,Rap/Hip Hop,Organ House,Jungle'
     .replace('\r', '').replace('\n', '').split(',')]
)
GROUPING = 'For Mixing'


def get_project_root() -> Path:
    return Path(__file__).parent


def check_filetype(files) -> list:
    result = []

    match filetype:
        case 'flac':
            mutagen_type = FLAC
            genre_fieldname = 'genre'

            def flac_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_key_name = 'grouping'
                grouping_tag_fieldname = 'GROUPING'
                if grouping_key_name in mutagen_audio.keys():
                    grouping_refined = str(mutagen_audio[grouping_tag_fieldname][0])
                    if grouping_refined == GROUPING:
                        return True

            grouping_field_exists_and_correct = flac_grouping_checker

        case 'm4a':
            mutagen_type = MP4
            genre_fieldname = '©gen'

            def m4a_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_fieldname = '----:com.apple.iTunes:GROUPING'
                if grouping_fieldname in mutagen_audio.keys():
                    grouping_raw = str(mutagen_audio['----:com.apple.iTunes:GROUPING'][0])
                    grouping_refined = grouping_raw[2:len(grouping_raw) - 1]
                    if grouping_refined == GROUPING:
                        return True

            grouping_field_exists_and_correct = m4a_grouping_checker

        case 'mp3':
            mutagen_type = EasyID3
            genre_fieldname = 'genre'

            def mp3_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_fieldname = 'GRP1'
                helper = ID3(mutagen_audio_filepath)
                if grouping_fieldname in helper.keys() and helper[grouping_fieldname] == GROUPING:
                    return True

            grouping_field_exists_and_correct = mp3_grouping_checker

        case 'ogg':
            mutagen_type = OggVorbis
            genre_fieldname = 'genre'

            def ogg_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_fieldname = 'grouping'
                if grouping_fieldname in mutagen_audio.keys():
                    grouping_refined = str(mutagen_audio[grouping_fieldname][0])
                    if grouping_refined == GROUPING:
                        return True

            grouping_field_exists_and_correct = ogg_grouping_checker

        case 'wav':
            mutagen_type = WAVE
            genre_fieldname = 'TCON'

            def wav_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_fieldname = 'GRP1'
                if grouping_fieldname in mutagen_audio.keys() and mutagen_audio[grouping_fieldname] == GROUPING:
                    return True

            grouping_field_exists_and_correct = wav_grouping_checker

        case _:
            print(f'\033[93mUndefined filetype \"{filetype}\"\033[0m\n')
            return result

    for relative_filepath in files:
        try:
            audio = mutagen_type(relative_filepath)
            is_correct_grouping = grouping_field_exists_and_correct(audio, relative_filepath)

            if genre_fieldname in audio.keys() and is_correct_grouping:
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
