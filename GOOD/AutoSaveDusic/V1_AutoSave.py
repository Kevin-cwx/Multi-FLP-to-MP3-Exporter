import os
import time
import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor
import pyautogui
import pygetwindow as gw

# Exports songs modified today to OneDrive Folder
"""
Dir where all FLP is store 
Dir output folder
FL Studio Path
Processor Type

"""
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects\K2"'\\'

List_Parent_FLP_Folder = [
    Root_Folder_K2+"2021",
    Root_Folder_K2+"2022",
    Root_Folder_K2+"2023",
    Root_Folder_K2+"2024"
]

Single_flp_Project_Path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects\K2\New Kev\black butterfly.flp"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 20"
Output_Folder_Path = r"C:\Users\Kfoen\Music\DropHere"
# Output_Folder_Path = r"C:\Users\Kfoen\OneDrive\Findusic"

Processor_Type = "FL64.exe"

# Closes FLStudio before code run
try:
    os.system("TASKKILL /F /IM ",Processor_Type)
except:
    print("Except ran")
    
# Gathers paths of all files within the specified directories
def get_file_paths(directory_paths):
    file_paths = []
    for directory_path in directory_paths:
        for filename in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, filename)):
                file_paths.append(os.path.join(directory_path, filename))
    return file_paths

# Export_FLP_to_MP3
def export_flp_to_mp3(file_path):
    Export_FLP_to_MP3 = f'cd {FL_Studio_Path} & {Processor_Type} /R /Emp3 "{file_path}" /O"{Output_Folder_Path}"'
    subprocess.call(Export_FLP_to_MP3, shell=True)
    #pyautogui.press('enter')

file_paths = get_file_paths(List_Parent_FLP_Folder)

today = datetime.date.today()
today_str = today.strftime("%d-%m-%Y")

file_paths_today = [file_path for file_path in file_paths if datetime.datetime.fromtimestamp(
    os.path.getmtime(file_path)).strftime("%d-%m-%Y") == today_str]

total_files = len(file_paths_today)
processed_files = 0

start_time = time.time()  # Start time before the export process starts

with ThreadPoolExecutor() as executor:
    futures = []
    for file_path in file_paths_today:
        futures.append(executor.submit(lambda path: export_flp_to_mp3(path), file_path))
        processed_files += 1
        # Print the correct file_path
        print(
            f"[{processed_files}/{total_files}] Exported {os.path.basename(file_path)}")
        #print(f"[{processed_files}/{total_files}] Exported {file_path}")  # Print the correct file_path


    # Wait for all tasks to complete
    for future in futures:
        future.result()
                
        # Check if FL Studio is the active program before pressing 'enter'
        if gw.getActiveWindowTitle() != 'FL Studio':
            fl_studio_window = gw.getWindowsWithTitle('FL Studio')
            if fl_studio_window:
                fl_studio_window[0].activate()

        #pyautogui.press('enter')

end_time = time.time()  # End time after all tasks have completed
total_elapsed_time = end_time - start_time

print("All modified FLP projects have been exported to:", Output_Folder_Path)
print(f"Total elapsed time: {total_elapsed_time:.2f} seconds")