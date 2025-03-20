import psutil
import os
import time

print("Manually open up your FL Studio")


def get_fl_studio_location():
    for process in psutil.process_iter(['pid', 'name', 'exe']):
        if process.info['name'] == 'FL64.exe':  # Change to 'FL.exe' for 32-bit
            return process.info['exe']


fl_studio_found = False
# Flag to ensure the message prints only once
fl_studio_not_running_printed = False

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
        if not fl_studio_not_running_printed:
            print("FL Studio is not running.")
            fl_studio_not_running_printed = True  # Prevent further prints

    time.sleep(1)  # Delay between checks
