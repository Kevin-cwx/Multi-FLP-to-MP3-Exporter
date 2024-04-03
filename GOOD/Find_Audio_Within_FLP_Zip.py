#Find audio tracks within a FLP project
import os
import zipfile

def read_zip_file(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        for file_name in file_list:
            print(file_name)

# Specify the path to your zip file
zip_file_path = r"C:\Users\Kfoen\Desktop\hard to fake.zip"

read_zip_file(zip_file_path)
#os.remove(zip_file_path)