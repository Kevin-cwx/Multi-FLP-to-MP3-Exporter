**Futre Feature**
Dark Mode
- Test if all text color are visible


Other
- Remove empty not a button below "Projects"


**Settings**
- Set output folder 
- Set input folder (Multiple, if not in same location)
- Set dark mode
- Set FL_Studio_Path ( Write function to find on own, but make editable)
- Set Processor_Type
-  Launch at system startup
- Toggle, auto export all projects you worked on today

If settings is empty (first time users), prompt user to run FL Studio, run code to get FL_Studio_Path and processes type, prompt user input fields for other values and store in json file
Save values for next run

**Search**
- Search input field, text should only show project in left side, and should open the folder if in sub folder
- It clashes with the color selection


**Styling**
- Make dark mode
- Change default to have a dark grey color




**Bugs**
1. Update status label
    1. Export 1 project, then export another project. Label gets overlapped.
    2. Added clear label in "def export_selected". 

