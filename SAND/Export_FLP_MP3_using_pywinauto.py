import pywinauto
from pywinauto.application import Application

# app = Application(backend='uia').start('notepad.exe').connect(title='Untitled - Notepad')
# app.UntitledNotepad.print_control_identifiers()

app = Application(backend='uia').start('"C:\\Program Files\\Image-Line\\FL Studio 20\\FL.exe"').connect(title='FL Studio 20')
app.FLStudio20.print_control_identifiers()



#C:\Program Files\Image-Line\FL Studio 20>FL.exe /R /Emp3 /F"C:\Users\Kfoen\Documents\Docs KF\FLPOutputMp3"
