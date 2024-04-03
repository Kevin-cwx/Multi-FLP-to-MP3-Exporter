import time
from pywinauto.application import Application
from pywinauto import Desktop

FLWin = Application(backend='uia').start(r"C:\Program Files\Image-Line\FL Studio 20\FL64.exe").connect(title='FL Studio 20',timeout=100)
time.sleep( 5 )

#FLWin = Desktop(backend='win32').window(title='FL Studio 20')
#print(FLWin.dump_tree())


