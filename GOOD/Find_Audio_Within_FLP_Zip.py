import zipfile
import os

def read_zip_file(zip_file_path):
    audio_extensions = ('.wav', '.mp3', '.flac', '.ogg', '.m4a', '.aac', '.wma', '.aiff', '.ape',
                        '.au', '.amr', '.dts', '.mka', '.mpc', '.opus', '.tta', '.voc', '.vorbis', '.webm')

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()

        for file_name in file_list:
            if file_name.lower().endswith(audio_extensions):
                print(os.path.basename(file_name))  # Print only the filename


# Specify the path to your zip file
zip_file_path = r"C:\Users\Kfoen\Desktop\dna.zip"

read_zip_file(zip_file_path)
