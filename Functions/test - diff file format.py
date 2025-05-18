import os
import subprocess

full_output_path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"
Output_Audio_Format = "Emp3"
file_path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2025\Huek.flp"

Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /{Output_Audio_Format} "{file_path}" /O"{full_output_path}"'
Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /Z "{file_path}" /O"{full_output_path}"'
subprocess.call(Export_FLP_to_MP3, shell=True)

