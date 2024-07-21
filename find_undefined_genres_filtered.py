import glob
from pathlib import Path

from colorama import just_fix_windows_console
from mutagen.easyid3 import EasyID3, EasyID3FileType
from mutagen.flac import FLAC
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


def check_filetype(files, filetype) -> tuple:
    result = []
    undefined_genres_summary_per_type = []

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
                grouping_fieldname_1 = '©grp'
                grouping_fieldname_2 = '----:com.apple.iTunes:GROUPING'
                if grouping_fieldname_1 in mutagen_audio.keys():
                    grouping_refined_1 = str(mutagen_audio[grouping_fieldname_1][0])
                    if grouping_refined_1 == GROUPING:
                        return True
                elif grouping_fieldname_2 in mutagen_audio.keys():
                    grouping_raw_2 = str(mutagen_audio[grouping_fieldname_2][0])
                    grouping_refined_2 = grouping_raw_2[2:len(grouping_raw_2) - 1]
                    if grouping_refined_2 == GROUPING:
                        return True

            grouping_field_exists_and_correct = m4a_grouping_checker

        case 'mp3':
            mutagen_type = EasyID3
            genre_fieldname = 'genre'

            def mp3_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_fieldname = 'grouping'
                helper = EasyID3FileType(mutagen_audio_filepath)
                if grouping_fieldname in helper.keys() and str(helper[grouping_fieldname][0]) == GROUPING:
                    return True

            grouping_field_exists_and_correct = mp3_grouping_checker

        case 'ogg':
            mutagen_type = OggVorbis
            genre_fieldname = 'genre'

            def ogg_grouping_checker(mutagen_audio, mutagen_audio_filepath) -> bool:
                grouping_fieldname_1 = 'grouping'
                grouping_fieldname_2 = 'contentgroup'
                if grouping_fieldname_1 in mutagen_audio.keys():
                    grouping_refined = str(mutagen_audio[grouping_fieldname_1][0])
                    if grouping_refined == GROUPING:
                        return True
                elif grouping_fieldname_2 in mutagen_audio.keys():
                    grouping_refined = str(mutagen_audio[grouping_fieldname_2][0])
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
            return result, undefined_genres_summary_per_type

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
