## **Futre Feature**



## **Other**
- ✅ - Remove empty not a button below "Projects"
- ✅ - Test with flp project embedded in multiple levels, not a single sub folder 
- Close folder, make it close per level, close all, close top subfolders
- Make a decision, should user be able to search for a folder?
    - if yes, then build functionality, for when a folder is searched, they are able to open the folder and view ALL files within (non filtered / hidden projects)
    -  ✅ - if no, then make sure flp with same name as folder is still visible
- Select projects via
    - Shift + Down Key
    - Ctrl + Down Key

## **Settings**
- Set output folder 
- Set input folder (Multiple, if not in same location)
- Set dark mode
- Set FL_Studio_Path ( Write function to find on own, but make editable)
- Set Processor_Type
-  Launch at system startup
- Toggle, auto export all projects you worked on today
- Enable Set output folder sub folder, User can name the sub folder within subfolder where they want to export songs
    - Create check if folde exists, else create folder
- Add about section, with version name
    - And disclaimer text, FL Studio must be closed. Show disclaimer 2 times, FLstudio must be closed before exporting song

- If settings is empty (first time users), prompt user to run FL Studio, run code to get FL_Studio_Path and processes type, prompt user input fields for other values and store in json file
 - Save values for next run
 - User can set mouse scroll speed 4 speeds. Normal, 2X, 3X, 5X

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
1. Update status label
    1. Export 1 project, then export another project. Label gets overlapped.
    2. Added clear label in "def export_selected". 



## **Exporting**
cd "C:\Program Files\Image-Line\FL Studio 21" 
FL64.exe /R /ogg "C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\616\Hue.flp" /O"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"


FL64.exe /Z"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects\2024\616\Hue.flp" /O"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"