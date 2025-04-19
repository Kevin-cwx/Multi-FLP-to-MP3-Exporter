import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import signal


class ReloadHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            print(f"\n🔁 Change detected: {event.src_path}")
            self.restart_process()

    def restart_process(self):
        # If there's an existing process running, stop it
        if self.process:
            print("🛑 Stopping previous instance...")
            self.stop_process()

        # Start a new process
        print("▶ Restarting app...")
        self.process = subprocess.Popen(self.command, shell=True)

    def stop_process(self):
        if self.process:
            try:
                # Send SIGTERM to gracefully terminate the process
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠ Process still running, force killing...")
                self.process.kill()
            finally:
                self.process = None


if __name__ == "__main__":
    # === Folder to watch ===
    watch_path = "C:\\Users\\Kfoen\\Documents\\Docs KF\\MyPythonProjects\\findusic\\GOOD\\AutoSaveDusic"

    # === Script to run ===
    command = 'python "C:\\Users\\Kfoen\\Documents\\Docs KF\\MyPythonProjects\\findusic\\GOOD\\AutoSaveDusic\\GUI FLP Exporter.py"'

    event_handler = ReloadHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()

    try:
        print("👀 Watching for changes... (Ctrl+C to stop)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Exiting...")
        observer.stop()
        # Ensure the current process is terminated
        if event_handler.process:
            event_handler.stop_process()

    observer.join()
