import subprocess

# Exports full mp3 song
#C:\\Users\\Kfoen\\Desktop\\aa.flp


Single_flp_Project_Path = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects\K2\New Kev\black butterfly.flp"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 20"
Output_Folder_Path = r"C:\Users\Kfoen\Music\DropHere"
Processor_Type = "FL64.exe"

#subprocess.call('cd C:\\Program Files\\Image-Line\\FL Studio 20 & FL64.exe /R /Emp3 "C:\\Users\\Kfoen\\Desktop\\aa.flp" /O"C:\\Users\\Kfoen\\Music\\DropHere\\"', shell=True)

Export_FLP_to_MP3 = f'cd {FL_Studio_Path} & {Processor_Type} /R /Emp3 "{Single_flp_Project_Path}" /O"{Output_Folder_Path}"'
subprocess.call(Export_FLP_to_MP3, shell=True)

print("done🔭")