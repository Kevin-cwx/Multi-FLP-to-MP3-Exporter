import os
import subprocess

full_output_path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"
file_path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2025\DC Tell Me.flp"

output_zip_path = os.path.join(full_output_path, os.path.basename(file_path))


#Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /{Output_Audio_Format} "{file_path}" /O"{full_output_path}"'
Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /Z"{file_path}" /O"{full_output_path}"'
#subprocess.call(Export_FLP_to_MP3, shell=True)


temp_flp_path = os.path.join(full_output_path, os.path.basename(file_path))
if not os.path.exists(temp_flp_path):
    # Copy FLP to output directory to trigger correct zip output path
    import shutil
    shutil.copy(file_path, temp_flp_path)

# Command to export that specific FLP as a ZIP
export_command = f'cd "{FL_Studio_Path}" & {Processor_Type} /Z"{temp_flp_path}"'
subprocess.call(export_command, shell=True)
os.remove(temp_flp_path)
