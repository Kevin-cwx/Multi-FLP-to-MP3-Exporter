import psutil
import os
import time

print("Open up FL Studio")

def get_fl_studio_location():
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        # Change this to 'FL.exe' if you're using FL Studio 32-bit
        if process.info['name'] == 'FL64.exe':
            return process.info['exe']


fl_studio_found = False

while not fl_studio_found:
    fl_studio_full_location = get_fl_studio_location()
    if fl_studio_full_location:
        Processor_Type = os.path.basename(fl_studio_full_location)
        FL_Studio_Path = os.path.dirname(fl_studio_full_location)
        print("FL Studio location:", fl_studio_full_location)
        print("Processor_Type:", Processor_Type)
        print("FL_Studio_Path:", FL_Studio_Path)
        fl_studio_found = True
    else:
        print("FL Studio is not running.")

    # Delay between each check (in seconds)
    time.sleep(4)  