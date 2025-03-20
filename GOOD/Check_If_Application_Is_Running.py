import time
import psutil

Counter = 1


def is_fl_studio_running():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'FL64.exe' in process.info['name']:
            return True
    return False


def run_until_stopped(Stop_After_In_Seconds=None):
    start_time = time.time()  # Get the current time
    is_fl_studio_running_initial = is_fl_studio_running()
    if is_fl_studio_running_initial:
        print("YES - FL Studio is running.")
    else:
        print("NO - FL Studio is not running.")

    while True:
        global Counter
        Counter += 1

        is_fl_studio_running_current = is_fl_studio_running()
        if is_fl_studio_running_current != is_fl_studio_running_initial:
            if is_fl_studio_running_current:
                print("YES - FL Studio is running.")
            else:
                print("NO - FL Studio is not running.")
            is_fl_studio_running_initial = is_fl_studio_running_current

        # Check if a time limit is provided and if the time has elapsed, break out of the loop
        if Stop_After_In_Seconds is not None and time.time() - start_time >= Stop_After_In_Seconds:
            break


# Call the function without providing Stop_After_In_Seconds (runs continuously)
# run_until_stopped()

# Call the function with a time limit of 6 seconds
run_until_stopped(19)
