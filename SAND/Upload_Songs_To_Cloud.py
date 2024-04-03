import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Path to the song file
my_song = r"C:\Users\Kfoen\Music\DropHere\buffalo city.mp3"

# Authenticate with Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Opens a web browser for authentication
#drive = GoogleDrive(gauth)

"""
# Create a new file on Google Drive
file_name = os.path.basename(my_song)
gdrive_file = drive.CreateFile({'title': file_name})
gdrive_file.SetContentFile(my_song)
gdrive_file.Upload()

# Print the link to access the uploaded file
print("Uploaded successfully! Access the song using the link below:")
print(gdrive_file['webContentLink'])


"""

