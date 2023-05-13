import os
from pydub import AudioSegment
from mutagen.flac import FLAC
from mutagen.wavpack import WavPack
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TCOM, TDRC, APIC

def insert_tags_to_mp3(new_file_path, title, artist, album, genre, year):
    mp3 = ID3(new_file_path)
    if title:
        mp3.add(TIT2(encoding=3, text=title))
    if artist:
        mp3.add(TPE1(encoding=3, text=artist))
    if album:
        mp3.add(TALB(encoding=3, text=album))
    if genre:
        mp3.add(TCON(encoding=3, text=genre))
    if year:
        mp3.add(TDRC(encoding=3, text=year))
    mp3.save()

def insert_art_to_mp3(new_file_path, art):
    try:
        mp3 = ID3(new_file_path)
        mp3.add(
            APIC(
                encoding=3,
                mime=art.mime,
                type=3,
                desc=u"Cover",
                data=art.data,
            )
        )
        mp3.save()
    except: print("{new_file_path}: Nepodařil se vložit obrázek")    

def tags_from_flac_to_mp3(file_path, new_file_path):
    flac = FLAC(file_path)
    title = flac.get("title", [""])[0]
    artist = flac.get("artist", [""])[0]
    album = flac.get("album", [""])[0]
    genre = flac.get("genre", [""])[0]
    year = flac.get("date", [""])[0]
    try:
        if flac.pictures != None: 
            art = flac.pictures[0]
            insert_art_to_mp3(new_file_path, art)
        insert_tags_to_mp3(new_file_path, title, artist, album, genre, year)
    except: "sx"
    
def tags_from_wav_to_mp3(file_path, new_file_path):
    wav = WavPack(file_path)
    title = wav.get("title", [""])[0]
    artist = wav.get("artist", [""])[0]
    album = wav.get("album", [""])[0]
    genre = wav.get("genre", [""])[0] 
    year = wav.get("date", [""])[0]
    try:
        if "APIC:" in wav:
            art= wav["APIC:"].data
            insert_art_to_mp3(new_file_path, art)
        insert_tags_to_mp3(new_file_path, title, artist, album, genre, year)
    except: "ex"
    

def find_conf_direc(direc):
    file = open("config/paths.txt", "r")
    for line in file:
        values = line.split(": ") 
        if values[0] == direc:
            return values[1] 

def chack_key(key):
    file = open("config/paths.txt", "r")
    for line in file:
        values = line.split(": ") 
        if values[0] == direc:
            return False
    return True

#potřeba dodělat#

def write_path_valus(key, value): 
    file = open("config/path.txt", "wr")

def rewrite_path_value(key, value):
    return 

#################

def configure_path_file():
    inserting = True
    while inserting:
        key = input("Zadej klíč cesty: ")
        value = input("Zadej cestu: ")
        if chack_key(key):
            write_path_valus(key, value)
        else:
            print("Tato hodnota je v souboru chcete ji přepsat?")
            rewrite = input("Chcete ji přepsat?(Y/N): ")
            if rewrite == "Y":
                rewrite_path_value(key, value)
        next_in = input("Chcete zadat další hodnotu?(Y/N):")
        if next_in == "N":
            inserting = False

def remuve_file(file_path):
    try: os.remove(file_path)
    except: print("Soubor nelze odsranit")

def connvert(direc, remuv):
    if remuv == "Y" or remuv == "y": 
        remuv = True
    else: remuv = False
    #if chack_key(direc):1
    #   direc = find_conf_direc(direc)
    #pro testovan
    #vsechny soubory do pole
    files = os.listdir(direc)
    #zacina connvertování
    for file in files:
        file_path = os.path.join(direc + file)
        if os.path.isdir(file_path):
            connvert(file_path + "/", remuv)
        if file.endswith(".flac"):
            audio = AudioSegment.from_file(file_path, format="flac")
            file_name = file[:-5]
            audio.export(direc + f"{file_name}.mp3", format="mp3", bitrate="320k")
            #potreba opravit 
            tags_from_flac_to_mp3(file_path, direc + f"{file_name}.mp3")
        elif file.endswith(".wav"):
            audio = AudioSegment.from_file(file_path, format="wav")
            file_name = file[:-4]
            audio.export(direc + f"{file_name}.mp3", format="mp3", bitrate="320k") 
            #potreba opravit 
            tags_from_wav_to_mp3(file_path, direc + f"{file_name}.mp3")
        if remuv:
            remuve_file(file_path)


direc = input("Složka kterou chcete convertovat:")
remuv = input("Chete odstranit predchozi soubory?(Y/N):")
connvert(direc, remuv)
