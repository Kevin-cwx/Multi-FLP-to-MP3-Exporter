#Set BPM info of a song in windows
import eyed3

# Load the audio file
audio_file = eyed3.load(r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\1more.mp3")

# Set the BPM value
bpm_value = 52  # Set your desired BPM value
audio_file.tag.bpm = bpm_value

# Save the changes
audio_file.tag.save()