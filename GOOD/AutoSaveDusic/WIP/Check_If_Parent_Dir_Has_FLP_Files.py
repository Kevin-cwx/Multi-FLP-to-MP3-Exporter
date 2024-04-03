from pathlib import Path


def check_for_flp_files(directory_path):
    # Create a Path object for the directory
    directory = Path(directory_path)

    # Use rglob to find .flp files in the directory and its subdirectories
    flp_files = list(directory.rglob('*.flp'))

    # Check if any .flp files were found
    if flp_files:
        print("Yes .flp files present.")
        # for flp_file in flp_files:
        #     print(flp_file)
    else:
        print("No .flp files found.")


a = 'C:/Users/Kfoen/Documents/Docs KF/MyPythonProjects'
b = 'C:/Users/Kfoen/Documents/Image-Line/FL Studio/Projects'
# Example usage
check_for_flp_files(a)