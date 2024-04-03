import zipfile
import os

def zip_flp_project(flp_folder_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root, _, files in os.walk(flp_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, flp_folder_path)
                zip_ref.write(file_path, relative_path)

# Specify the path to your FL Studio project folder
flp_folder_path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects\K2\2023\MWM.flp"

# Specify the path for the resulting zip file, including the file name and extension
zip_file_path = r"C:\Users\Kfoen\Desktop\project.zip"

zip_flp_project(flp_folder_path, zip_file_path)
