import os
import datetime
from tabulate import tabulate

def get_file_paths(directory_paths):
    table_data = []

    for directory_path in directory_paths:
        file_paths = []
        for filename in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, filename)):
                file_paths.append(os.path.join(directory_path, filename))
        
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%d-%m-%Y %H:%M:%S")
            table_data.append([file_name, file_path, modified_time])

    return table_data

# Define a list of directory paths
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects\K2\\"
#Directory_Paths = [Root_Folder_K2 + "2023", Root_Folder_K2 + "2022"]
Directory_Paths = [Root_Folder_K2 + "2023"]


# Get file paths and create the table data
table_data = get_file_paths(Directory_Paths)

# Define column names
col_names = ["File Name", "Full Path", "Modified Time"]

# Print the table and list count
print(tabulate(table_data, headers=col_names))
print("List Count:", len(table_data))
