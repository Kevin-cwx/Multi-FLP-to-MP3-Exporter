from pyflp import FLProject
import sys

# Replace this with the path to your FLP file
flp_path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\BEYKEL\Web.flp"

try:
    project = FLProject.load(flp_path)
    print(f"FL Studio Version: {project.fl_version}")
    print(f"Project Title: {project.title}")
    print(f"Number of Channels: {len(project.channels)}")
    print(f"Number of Patterns: {len(project.patterns)}")

    print("\n=== Channels ===")
    for i, channel in enumerate(project.channels):
        print(f"{i+1}. {channel.name}")

    print("\n=== Patterns ===")
    for i, pattern in enumerate(project.patterns):
        print(f"{i+1}. {pattern.name}")

except Exception as e:
    print(f"Error loading FLP: {e}")
    sys.exit(1)
