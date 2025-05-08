## **Current Task**
- Implement - if FL64.exe fails, then try FL.exe, and vice versa
- organize code, multiple, SCROLL_SPEED_MAPPING
- 


## **Other**
- Remove empty not a button below "Projects"
- Define tab order
- Predefined group of projects  - that can be added in selected project via one click
- Increase size of checkbox in settings

- Package app
- Test on other machine
- Add themes functionality
- ✅ - Add settings functionality, save and get values from ini file

- Figure out how to be able to save a output folder with name "♬", need to escape characters in save_config

- ✅ - First run window, make FL installation path text selectable, also in settings
- ✅ - Let FLP projects folder be shown underneath each other
- Enable check, on save settings, mandatory fields must be filled in, Output folder, FLP projects folder, FL studio path. Check before saving current to ini file, that way you still auto set paths for user
- Need to clear search entry after projects are synced


## **Settings**
#### General 
#### Items to have
- ✅ - Set output folder 
- ✅ - Set input folder (Multiple, if not in same location)
- Launch at system startup
- ✅ -  Project_Order_By, toggle name or date

#### Advanced
- ✅ -  Set FL_Studio_Path ( Write function to find on own, but make editable)
- Set Processor_Type
- ❌ - Toggle, enable auto export all projects you worked on today
    - No need to build this. Users can just click recent projects
- ✅ - Enable Set output folder sub folder, User can name the sub folder within subfolder where they want to export songs
- User can set mouse scroll speed 4 speeds. Normal, 2X, 3X, 5X


- Make advanced closable (default)
- Add change font size for projects and selected projects (padding must also be changed in background)

## **Future Feature**
- 



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

- Input fields should be white, in settings and also on mainwindow
    - or only in settings, and on main window make border bold as indicator
    - currently, ony when output subfolder is created, does it change for all other inputs


## **Bugs**
- Figure out how to prevent FLP from exporting pattern instead of full song
    - If FLP is added to pattern it exports as pattern, if project is closed on song mode then it exports as song.
- Settings, output folder, when a new folder is added - it does not show the new folder in the input frame
- Font size should be calculated as on home laptop size of font gets clipped while not the case on work pc
- After clicking "save settings" it does not go back


---
## **Done**
- ✅ - Test with flp project embedded in multiple levels, not a single sub folder 
- ❌ - Close folder, make it close per level, close all, close top subfolders
    - What if there's a hundred top levels?
- ✅ - Make a decision, should user be able to search for a folder?
    - if yes, then build functionality, for when a folder is searched, they are able to open the folder and view ALL files within (non filtered / hidden projects)
    -  ✅ - if no, then make sure flp with same name as folder is still visible
- ✅ - Select projects via
    - Shift + Down Key
    - Ctrl + Down Key
    - No unselect
- ✅ - Change background color of selected project section
- ✅ - Logic for enable output subfolder in settings
    - First time user - Set to false
    - this is preventing "save settings"
- ✅ - Fix after i search for a project and i go in settings, and then click save settings. Once i return to the main window, i want to be able to see my last search results, thus search entry needs to be populated correctly, and the correct items i search need to be shown in project tree

## **Search**
- ✅ - Search input field, text should only show project in left side, and should open the folder if in sub folder

## **First Time Setup**
- ✅ - Window with 
    - FL input folder
    - FL output folder
    - FL Path
    - Processor type
- ✅ - function to autofind info


## Settings
- ✅ -If settings is empty (first time users), prompt user to run FL Studio, run code to get FL_Studio_Path and processes type, prompt user input fields for other values and store in json file
 - ✅ -Save values for next run
- ❌ - Create button, go to input folder
    - No need as user can open file and flp location folder via right click


## **Bugs**
- ✅ - Update status label
    1. Export 1 project, then export another project. Label gets overlapped.
    2. Added clear label in "def export_selected". 
- ✅ - When sync is clicked, and I manually close the folders, it did not update  the close folder button, when i clicked sync again
    - Set beahviour, when sync is clicked always open all folders
- ✅ - Original Sync button does not take same location once settings is clicked again
- ✅ - Add right click on folder also, to open folder location
✅ - First time user - Setup works, values are saved in ini file
    - However once ok is clicked, program does not open main window
- ✅ - Disable scroll for all dropdowns
    -   As it causes accidental value changes, only allow explicit opening ofdropdown and value selection


#### About
- ✅ - Add about section, with version name
    - And disclaimer text, FL Studio must be closed. Show disclaimer 2 times, FLstudio must be closed before exporting song



## **Exporting**
cd "C:\Program Files\Image-Line\FL Studio 21" 
FL64.exe /R /ogg "C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\616\Hue.flp" /O"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"


FL64.exe /Z"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\616\Hue.flp" /O"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"

---
Watchdog
Run in GUI.py dir
watchmedo auto-restart --patterns="*.py" --recursive -- python GUI.py

If it fails, move file back to Good/A dir

**First Time User**
C:\Users\Kfoen