import os
import time
import datetime
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor
import pyautogui
import pygetwindow as gw

# Exports songs modified today to OneDrive Folder
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"

FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Output_Folder_Path = r"C:\Users\Kfoen\Music\DropHere"
Processor_Type = "FL64.exe"

# Closes FLStudio before code runs
try:
    os.system(f"TASKKILL /F /IM {Processor_Type}")
except:
    print("")

# Recursively search for all .flp files in Root_Folder_K2, skipping "Backup" folders


def get_file_paths(root_directory):
    file_paths = set()  # Use a set to avoid duplicate file paths
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Skip folders named "Backup"
        if "Backup" in dirpath.split(os.sep):
            continue

        for filename in filenames:
            if filename.lower().endswith(".flp"):  # Ensure case insensitivity
                file_paths.add(os.path.join(dirpath, filename))
    return list(file_paths)  # Convert back to list

# Remove overwritten or duplicate versions of the same file


def filter_unique_files(file_paths):
    clean_files = {}

    for file_path in file_paths:
        base_name = os.path.basename(file_path)

        # Remove timestamps or "(overwritten at ...)" from filenames
        simplified_name = re.sub(r'\s*\(.*?\).*', '', base_name).strip()

        # Only keep the simplest version of the file
        if simplified_name not in clean_files or len(base_name) < len(clean_files[simplified_name]):
            clean_files[simplified_name] = file_path

    return list(clean_files.values())

# Export FLP to MP3


def export_flp_to_mp3(file_path):
    Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /Emp3 "{file_path}" /O"{Output_Folder_Path}"'
    subprocess.call(Export_FLP_to_MP3, shell=True)


file_paths = get_file_paths(Root_Folder_K2)

# Filter only the files modified today
today = datetime.date.today()
today_str = today.strftime("%d-%m-%Y")

file_paths_today = list(set(
    file_path for file_path in file_paths
    if datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%d-%m-%Y") == today_str
))

# Apply filtering to remove duplicate/overwritten versions
file_paths_today = filter_unique_files(file_paths_today)

total_files = len(file_paths_today)
processed_files = 0

if total_files > 0:
    start_time = time.time()  # Start time before the export process starts

    with ThreadPoolExecutor() as executor:
        futures = []
        for file_path in file_paths_today:
            futures.append(executor.submit(export_flp_to_mp3, file_path))
            processed_files += 1
            print(
                f"[{processed_files}/{total_files}] Exported {os.path.basename(file_path)}")

        # Wait for all tasks to complete
        for future in futures:
            future.result()

            # Check if FL Studio is the active program before pressing 'enter'
            if gw.getActiveWindowTitle() != 'FL Studio':
                fl_studio_window = gw.getWindowsWithTitle('FL Studio')
                if fl_studio_window:
                    fl_studio_window[0].activate()

    end_time = time.time()  # End time after all tasks have completed
    total_elapsed_time = end_time - start_time

    print("All modified FLP projects have been exported to:", Output_Folder_Path)
    print(f"Total elapsed time: {total_elapsed_time:.2f} seconds")
