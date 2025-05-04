## **Futre Feature**



## **Other**
-  - Remove empty not a button below "Projects"
- ✅ - Test with flp project embedded in multiple levels, not a single sub folder 
- ❌ - Close folder, make it close per level, close all, close top subfolders
    - What if there's a hundred top levels?
- Make a decision, should user be able to search for a folder?
    - if yes, then build functionality, for when a folder is searched, they are able to open the folder and view ALL files within (non filtered / hidden projects)
    -  ✅ - if no, then make sure flp with same name as folder is still visible
- ✅ - Select projects via
    - Shift + Down Key
    - Ctrl + Down Key
    - No unselect
- Define tab order
- Predefined group songs - that can be added in selected project
- Increase size of checkbox

- Save settings, so that on restart it uses previous stored settings
- Package app
- Test on other machine
- Add themes functionality
- Add settings functionality, save and get values from ini file
- Change background color of selected project section



## **Settings**
#### General
- Set output folder 
- Set input folder (Multiple, if not in same location)
- Launch at system startup
- Project_Order_By, toggle name or date

#### Advanced
- Set FL_Studio_Path ( Write function to find on own, but make editable)
- Set Processor_Type
- ❌ - Toggle, enable auto export all projects you worked on today
    - No need to build this. Users can just click recent projects
- Enable Set output folder sub folder, User can name the sub folder within subfolder where they want to export songs
- User can set mouse scroll speed 4 speeds. Normal, 2X, 3X, 5X

- If settings is empty (first time users), prompt user to run FL Studio, run code to get FL_Studio_Path and processes type, prompt user input fields for other values and store in json file
 - Save values for next run
- ❌ - Create button, go to input folder
    - User can open file and flp location folder via right click

- Make advanced closable (default)
- Add change font size for projects and selected projects (padding must also be changed in background)


#### About
- ✅ - Add about section, with version name
    - And disclaimer text, FL Studio must be closed. Show disclaimer 2 times, FLstudio must be closed before exporting song


## **First Time Setup**
- ✅ - Window with 
    - FL input folder
    - FL output folder
    - FL Path
    - Processor type
- ✅ - function to autofind info



## **Search**
- ✅ - Search input field, text should only show project in left side, and should open the folder if in sub folder


## **Styling**
- Make color themes
    - Dark Mode
    - Cherry 
    - Sky Blue
    - Default
    - FL Skin
    - Barbie 
    - Forest Green
    - Brazil Tan
    - Default
- Change default to have a dark grey color




## **Bugs**
1. ✅ - Update status label
    1. Export 1 project, then export another project. Label gets overlapped.
    2. Added clear label in "def export_selected". 
2. ✅ - When sync is clicked, and I manually close the folders, it did not update  the close folder button, when i clicked sync again
    - Set beahviour, when sync is clicked always open all folders
3. ✅ - Original Sync button does not take same location once settings is clicked again
4. ✅ - Add right click on folder also, to open folder location
5. Figure out how to prevent FLP from exporting pattern instead of full song
    - If FLP is added to pattern it exports as pattern, if project is closed on song mode then it exports as song.
6. First time user - Setup works, values are saved in ini file
    - However once ok is clicked, program does not open main window



## **Exporting**
cd "C:\Program Files\Image-Line\FL Studio 21" 
FL64.exe /R /ogg "C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\616\Hue.flp" /O"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"


FL64.exe /Z"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\616\Hue.flp" /O"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"

---
Watchdog
Run in GUI.py dir
watchmedo auto-restart --patterns="*.py" --recursive -- python GUI.py

If it fails, move file back to Good/A dir