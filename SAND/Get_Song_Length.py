from mutagen.mp3 import MP3


"""
From Parent_Folder, copy all files to a temp_folder
Get BPM from flp files
Save to Dictionary
Add BPM info to modified Dictionary
Set to song info
Display on tkinter

"""


def get_audio_length(file_path):
    audio = MP3(file_path)
    length_in_sec = audio.info.length
    minutes, seconds = divmod(length_in_sec, 60)
    return int(minutes), int(seconds)

# Example usage
audio_file_path = r"C:\Users\Kfoen\Music\DropHere\TIME OUT.mp3"
minutes, seconds = get_audio_length(audio_file_path)
print(f"{minutes}:{seconds}")
