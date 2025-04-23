import psutil
import win32gui
import win32process


def close_fl_studio():
    def enum_windows_callback(hwnd, pid_list):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if "FL Studio" in window_title:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                pid_list.append(pid)

    fl_pids = []
    win32gui.EnumWindows(enum_windows_callback, fl_pids)

    for pid in set(fl_pids):
        try:
            proc = psutil.Process(pid)
            print(f"Terminating: {proc.name()} (PID: {pid})")
            proc.terminate()
            proc.wait(timeout=5)
        except Exception as e:
            print(f"Failed to terminate PID {pid}: {e}")



