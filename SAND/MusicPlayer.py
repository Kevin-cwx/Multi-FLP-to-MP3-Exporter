import os
from tkinter import *
from pygame import mixer

def play_song(song_path):
    mixer.music.load(song_path)
    mixer.music.play()

def pause_song():
    mixer.music.pause()

def load_songs(directory):
    songs = []
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            songs.append(filename)
    return songs

def create_music_player(directory):
    # Load songs from the directory
    songs = load_songs(directory)

    # Create the main window
    window = Tk()
    window.title("Music Player")

    # Create a listbox to display the songs
    listbox = Listbox(window, width=50)
    listbox.pack()

    # Populate the listbox with songs
    for song in songs:
        listbox.insert(END, song)

    # Create a button to play the selected song
    def play_selected_song():
        selection = listbox.curselection()
        if selection:
            song_index = int(selection[0])
            song_path = os.path.join(directory, songs[song_index])
            play_song(song_path)

    play_button = Button(window, text="Play", command=play_selected_song)
    play_button.pack()

    # Create a button to pause the music
    pause_button = Button(window, text="Pause", command=pause_song)
    pause_button.pack()

    # Initialize the mixer
    mixer.init()

    # Run the main window loop
    window.mainloop()

# Usage example
music_directory = r"C:\Users\Kfoen\Music\DropHere"
create_music_player(music_directory)