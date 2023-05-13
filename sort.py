import os
import mutagen
from mutagen import mp3


from_dir = 'C:/Users/kubex/documents/Soulseek Downloads/'
to_dir = 'F:/REE MUSIC/'
files = os.listdir(from_dir)


def get_autor(file):
    if file.endswith(".mp3"):
        audio = mp3.MP3(file)
        return audio.tags["TPE1"]

def swap_word(array, delete, insert):
    result = ""
    for i in range(len(array)):
        for word in delete:
            if array[i] == word:
                array[i] = insert
        result += array[i]
    return result

def get_main_autor(autor):
    autor = str(autor).split()
    autor = swap_word(autor, ["x", "&", ".feat"], "|")
    return autor

def find_folder(to_dir, autor):
    if "0" <= autor[0] <= "9":
        return to_dir + "/VA - NUMBERS"
    elif autor[0] < "F":
        return to_dir + "/VA - A-F"
    elif autor[0] < "M":
        return to_dir + "/VA - G-L"
    elif autor[0] < "S":
        return to_dir + "/VA - M-R"
    else:
        return to_dir + "/VA - S-Z"

def insert_to_folder(to_dir, file, autor):
    final_folder = find_folder(to_dir, autor)
    files = os.listdir(final_folder)
    for file in files:
        print(file)


def sort(from_dir, to_dir):
    files = os.listdir(from_dir)
    for file in files:
        if os.path.isdir(from_dir + file):
            sort(from_dir + file + "/", to_dir)
        try:
            autor = get_autor(from_dir + file)
            autor = get_main_autor(autor)
            if(autor != None):
                insert_to_folder(to_dir, from_dir + file, autor)
        except mp3.HeaderNotFoundError:
            print(f"{file}: nemá tagy")
        except mutagen.MutagenError:
            print(f"{file}: nemáte přístup")
        except:
            print(f"{file}: vznikla chyba")


sort(from_dir, to_dir)
