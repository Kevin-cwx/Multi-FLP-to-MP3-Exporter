import os
import re
import subprocess
import ttkbootstrap
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import Listbox
import tkinter as tk
import datetime
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip
import psutil
import win32gui
import win32process
from tkinter import messagebox
from tkinter import filedialog
import winreg
import sys
from tkinter import PhotoImage
import time


global Output_Folder_Path
global Project_Order_By
# === CONFIG ===
USE_DARK_MODE = False
#Dir_FLP_Projects = r"C:\Users\foendoe.kevin\Documents\findusic - FLP Input"

Dir_FLP_Projects = [
    # r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 12 - projects",
    # r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects",
    # r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
    r"C:\Users\foendoe.kevin\Documents\findusic - FLP Input"
]
Output_Folder_Path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"

Search_Placeholder_Text = "Search Projects"
Project_Order_By = "name"  #date, name
global Set_Output_Sub_Folder
Set_Output_Sub_Folder = False
Output_Sub_Folder_Name = ""
Output_Sub_Folder_Name = ""
Output_Audio_Format = "Emp3"
Mouse_Scroll_Speed = 7
Application_Name = "Multi FLP to MP3 Exporter"
Launch_At_Startup = False
Font_Name = "Helvetica"
# Emp3,ogg,wav
#ogg does not work in powershell, FL might have disabled

#
# Colors
#
Selected_Project_Background_Color = "#2fbdff"
Selected_Project_Text_Color = "black"
Selected_Project_Window_Background_Color = "#77f190"

Top_Title_Color = "black"
Search_Placeholder_Text_Color = "black"
Project_Color_Tree = "white"
Background_Color = "#cee4ff"
Project_Tree_Background_Color = "white"
Project_Tree_Text_Color = "black"
"""
#34b1eb
#8a9296
"""
# ---

# === THEMES ===
THEME_NAMES = [
    "Dark Mode", "Cherry", "Sky Blue", "Default", "FL Skin", "Barbie",
    "Forest Green", "Brazil Tan"
]


def get_file_paths(root_directories):
    file_paths = {}
    if isinstance(root_directories, str):
        root_directories = [root_directories]

    for root_directory in root_directories:
        for dirpath, dirnames, filenames in os.walk(root_directory):
            if "Backup" in dirpath.split(os.sep):
                continue
            for filename in filenames:
                if filename.lower().endswith(".flp"):
                    file_path = os.path.join(dirpath, filename)
                    modified_date = os.path.getmtime(file_path)
                    file_paths[file_path] = modified_date
    return file_paths


def close_fl_studio():
    try:
        # Method 1: Using taskkill with the process name
        os.system("taskkill /f /im FL64.exe")  # For 64-bit version
        os.system("taskkill /f /im FL.exe")  # For 32-bit version

        # Alternative Method 2: Using psutil (more elegant)
        try:
            import psutil
            for proc in psutil.process_iter():
                if proc.name().lower() in ['fl64.exe', 'fl.exe']:
                    proc.kill()
        except ImportError:
            pass

        return True
    except Exception as e:
        return False


def export_flp_to_mp3(file_path):
    global Output_Folder_Path
    close_fl_studio()
    # Get subfolder name if enabled
    if Set_Output_Sub_Folder:
        subfolder = app.subfolder_entry.get().strip()
        if subfolder:
            # Create full output path with subfolder
            full_output_path = os.path.join(Output_Folder_Path, subfolder)

            # Create directory if it doesn't exist
            if not os.path.exists(full_output_path):
                try:
                    os.makedirs(full_output_path)
                except OSError as e:
                    print(f"Error creating subfolder: {e}")
                    full_output_path = Output_Folder_Path  # Fallback to main folder
        else:
            full_output_path = Output_Folder_Path
    else:
        full_output_path = Output_Folder_Path

    Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /{Output_Audio_Format} "{file_path}" /O"{full_output_path}"'
    #print(Export_FLP_to_MP3)
    subprocess.call(Export_FLP_to_MP3, shell=True)


class FLPExporterUI:

    def __init__(self, root):
        self.root = root
        self.root.title(Application_Name)
        self.root.geometry("600x700+30+20")
        self.root.minsize(520, 550)
        #self.root.geometry("600x700+30+20")
        self.root.resizable(True, True)
        transparent_icon = tk.PhotoImage(width=1, height=1)
        self.root.iconbitmap(r"Media/Icons/FL21 - Icon.ico")
        # white
        self.root.configure(bg=Background_Color)
        self.folders_expanded = True
        self.settings_open = False
        style = ttk.Style()
        style.configure('TLabel', background=Background_Color)
        style.configure('success.TLabel', background=Background_Color)
        # Define hot pink background
        style.configure('HotPink.TFrame', background=Background_Color)
        style.configure('Settings.TFrame', background=Background_Color)
        style.configure('Settings.TEntry', fieldbackground=Background_Color)
        style.configure('Settings.TLabel', background=Background_Color)
        style.configure('Settings.TCheckbutton', background=Background_Color)
        style.configure('Settings.TCombobox', fieldbackground=Background_Color)

        self.root.config(bg=Background_Color)
        self.root.update_idletasks()
        # 2. Apply the style to the top bar frame
        # Use the custom style
        self.top_bar = ttk.Frame(self.root, style='HotPink.TFrame')
        self.top_bar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Add heading to the top bar frame (left side)
        self.heading = ttk.Label(self.top_bar,
                                 text=f"🎵 {Application_Name}",
                                 font=(Font_Name, 16, "bold"),
                                 bootstyle="info",
                                 foreground=Top_Title_Color,
                                 background=Background_Color)
        self.heading.pack(side=tk.LEFT, pady=0)

        self.download_icon = self.load_icon("Media/Icons/download.png")
        self.plus_icon = self.load_icon("Media/Icons/plus.png")
        self.minus_icon = self.load_icon("Media/Icons/minus.png")
        self.clear_icon = self.load_icon("Media/Icons/clear.png")
        self.recent_icon = self.load_icon("Media/Icons/recent.png")
        self.settings_icon = self.load_icon("Media/Icons/settings.png")
        self.music_folder_icon = self.load_icon("Media/Icons/musical-note.png")
        self.sync_icon = self.load_icon("Media/Icons/sync.png")

        self.selected_files = set()
        self.path_map = {}
        self.last_selected_item = None
        self.all_items = {}
        self.original_tree_state = {}

        self.content_frame = ttk.Frame(self.root, style='HotPink.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.left_frame = ttk.Frame(self.content_frame, style='HotPink.TFrame')
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add search frame
        search_frame = ttk.Frame(self.left_frame,
                                 borderwidth=2,
                                 relief='solid')
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 0))

        style = ttk.Style()
        style.configure("Search.TEntry", relief="flat")

        self.search_entry = ttk.Entry(search_frame, style="Search.TEntry")
        self.search_entry.pack(side=tk.LEFT,
                               fill=tk.X,
                               expand=True,
                               padx=(0, 0))

        # Output Sub Folder
        if Set_Output_Sub_Folder:
            # Create a new frame below the search frame
            self.subfolder_frame = ttk.Frame(self.left_frame)
            self.subfolder_frame.pack(fill=tk.X, padx=5, pady=(5, 0))

            self.subfolder_label = ttk.Label(self.subfolder_frame,
                                             text="Output Subfolder:",
                                             background="white")
            self.subfolder_label.pack(side=tk.LEFT, padx=(0, 5))

            self.subfolder_entry = ttk.Entry(self.subfolder_frame)
            self.subfolder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.subfolder_entry.insert(0, Output_Sub_Folder_Name)

        # Add placeholder text and configure events
        self.search_entry.insert(0, Search_Placeholder_Text)
        self.search_entry.config(foreground=Search_Placeholder_Text_Color)
        self.placeholder_active = True
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_entry.bind("<KeyRelease>", self.filter_tree)

        self.close_button = ttk.Button(
            self.top_bar,
            text="Cancel",
            command=self.close_settings_without_saving,
            bootstyle="outline-danger")

        self.search_entry.bind("<KeyRelease>", self.filter_tree)

        self.tree_label = ttk.Label(self.left_frame,
                                    text="Projects",
                                    font=(Font_Name, 14, "bold"),
                                    background=Background_Color)
        self.tree_label.pack(pady=(10, 0), anchor='w', fill='x', padx=0)

        self.instruction_label = ttk.Label(
            self.left_frame,
            text="Double click to select / unselect projects",
            font=(Font_Name, 14),
            background=Background_Color  # Add this line
        )
        self.instruction_label.pack(pady=(1, 1), anchor='w', fill='x')

        tree_frame = ttk.Frame(self.left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

        # Increase size of projects
        #  rowheight=20
        style.configure(
            "Custom.Treeview",
            
            background=Project_Tree_Background_Color,
            fieldbackground="#f0f0f0",  
            foreground=Project_Tree_Text_Color,  # Text color
            font=(Font_Name, 9))
        # Projects Left Side
        self.tree = ttk.Treeview(
            tree_frame,
            selectmode="extended",
            style="Custom.Treeview"  # Use the custom style
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.anchor_item = None
        self.last_direction = None
        self.tree.bind("<MouseWheel>", self.on_mousewheel)
        self.tree.bind("<Button-4>", self.on_mousewheel)
        self.tree.bind("<Button-5>", self.on_mousewheel)
        self.tree.bind("<Control-Shift-Up>", self.on_ctrl_shift_arrow)
        self.tree.bind("<Control-Shift-Down>", self.on_ctrl_shift_arrow)
        self.tree.bind("<KeyRelease>", self.reset_anchor)

        scrollbar = ttk.Scrollbar(tree_frame,
                                  orient="vertical",
                                  command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.tag_configure("selected",
                                background=Selected_Project_Background_Color,
                                foreground=Selected_Project_Text_Color)

        # Add right-click binding to the tree
        self.tree.bind("<Button-3>", self.on_right_click)

        self.right_frame = ttk.Frame(self.content_frame,
                                     style='HotPink.TFrame')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        self.cart_label = ttk.Label(self.right_frame,
                                    text="Selected Projects",
                                    font=(Font_Name, 12, "bold"),
                                    background=Background_Color)
        self.cart_label.pack(pady=(0, 0), anchor='w', fill='x', padx=10)

        self.cart_listbox = Listbox(
            self.right_frame,
            height=15,
            width=40,
            selectmode=tk.SINGLE,
            selectbackground="#fd4545",  # Light gray (match left tree)
            fg="red",  # Text color
            font=(Font_Name, 10))
        self.cart_listbox.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.cart_listbox.bind("<Double-Button-1>", self.on_cart_double_click)

        self.export_button = ttk.Button(self.right_frame,
                                        text="Export",
                                        image=self.download_icon,
                                        compound=tk.LEFT,
                                        command=self.export_selected,
                                        bootstyle="success")
        self.export_button.pack(pady=5, padx=20, fill=X)

        self.enter_button = ttk.Button(self.right_frame,
                                       text="Select",
                                       image=self.plus_icon,
                                       compound=tk.LEFT,
                                       command=lambda: self.on_enter_key(None),
                                       bootstyle="outline-info")
        self.enter_button.pack(pady=5, padx=20, fill=X)

        self.clear_button = ttk.Button(self.right_frame,
                                       text="Clear All",
                                       image=self.clear_icon,
                                       compound=tk.LEFT,
                                       command=self.clear_selection,
                                       bootstyle="info-outline")
        self.clear_button.pack(pady=(0, 5), padx=20, fill=X)

        self.add_today_button = ttk.Button(self.right_frame,
                                           text="Recent",
                                           image=self.recent_icon,
                                           compound=tk.LEFT,
                                           command=self.add_recent_projects,
                                           bootstyle="outline-info")
        self.add_today_button.pack(pady=(5, 5), padx=20, fill=X)
        # outline-secondary

        # Settings button
        self.settings_button = ttk.Button(self.top_bar,
                                          text="Settings",
                                          image=self.settings_icon,
                                          command=self.open_settings,
                                          bootstyle="outline-info")
        self.settings_button.pack(side=tk.RIGHT)
        self.settings_tip = Hovertip(self.settings_button, 'Settings')

        self.toggle_icon = self.minus_icon
        self.toggle_button_Close_Folders = ttk.Button(
            self.top_bar,
            image=self.toggle_icon,
            compound=tk.LEFT,
            command=self.toggle_folders,
            bootstyle="outline-info")

        # Create the Music Output Folder button next to toggle button
        self.output_music_folder_button = ttk.Button(
            self.top_bar,
            image=self.music_folder_icon,
            compound=tk.LEFT,
            command=self.open_output_folder,
            bootstyle="outline-info")
        self.output_music_folder_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.music_folder_tip = Hovertip(self.output_music_folder_button,
                                         'Open MP3 Output Folder')

        self.sync_button = ttk.Button(self.top_bar,
                                      image=self.sync_icon,
                                      compound=tk.LEFT,
                                      command=self.sync_projects,
                                      bootstyle="outline-info")

        self.sync_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.sync_tip = Hovertip(self.sync_button,
                                 'Sync and update project tree')

        self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))
        self.toggle_tip = Hovertip(self.toggle_button_Close_Folders,
                                   'Close folders')

        self.status_label = ttk.Label(self.right_frame,
                                      text="",
                                      font=(Font_Name, 11),
                                      bootstyle="success",
                                      background=Background_Color)
        self.status_label.pack(pady=(0, 10))

        self.populate_tree(Dir_FLP_Projects)
        self.root.bind("<Return>", self.on_enter_key)

        # Taskbar_Image = Image.open('Media/Icons/a.jpg')
        # Taskbar_Image.save('Media/a.ico', format='ICO', sizes=[(32, 32), (64, 64)])
        # # Set taskbar icon (works for Windows)
        # self.root.iconbitmap('Media/a.ico')  # Add this line

    def on_search_focus_in(self, event):
        """Handle focus in event to remove placeholder text"""
        if self.placeholder_active:
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground='black')
            self.placeholder_active = False

    def on_search_focus_out(self, event):
        """Handle focus out event to restore placeholder text if empty"""
        if not self.search_entry.get():
            self.search_entry.insert(0, Search_Placeholder_Text)
            self.search_entry.config(foreground=Search_Placeholder_Text_Color)
            self.placeholder_active = True
        else:
            self.placeholder_active = False

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        try:
            if os.path.exists(Output_Folder_Path):
                os.startfile(Output_Folder_Path)
            else:
                print("Output folder not found")
        except Exception as e:
            print(f"Error opening folder: {str(e)}")

    def filter_tree(self, event):
        search_term = self.search_entry.get().lower()

        # Check if placeholder is active
        if self.placeholder_active:
            search_term = ""
        else:
            search_term = self.search_entry.get().lower()

        # If search term is empty, restore original tree state
        if not search_term:
            # First show all items
            for item in self.tree.get_children():
                self.show_item_and_children(item)

            # Then restore original state
            if not self.original_tree_state:
                self.store_tree_state()
            self.restore_tree_state()
            return

        # Store current tree state if not already stored
        if not self.original_tree_state:
            self.store_tree_state()

        # First, hide all items
        for item in self.tree.get_children():
            self.hide_item_and_children(item)

        # Show matching FLP files and their parent folders
        for item_id, item_text in self.all_items.items():
            if item_id in self.path_map and search_term in item_text.lower():
                # Show the matching item and its parents
                self.show_item_and_parents(item_id)

                # Also show siblings if parent folder matches
                parent = self.tree.parent(item_id)
                if parent:
                    for sibling in self.tree.get_children(parent):
                        if sibling in self.path_map:
                            self.tree.reattach(sibling, parent, 'end')

        # Additionally show folders that contain matches
        for item_id in self.tree.get_children():
            if any(search_term in self.all_items[child].lower()
                   for child in self.tree.get_children(item_id)
                   if child in self.path_map):
                self.tree.reattach(item_id, self.tree.parent(item_id), 'end')
                self.tree.item(item_id, open=True)

    def store_tree_state(self):
        """Store the original expanded/collapsed state of all items."""
        self.original_tree_state = {}
        for item in self.tree.get_children():
            self.store_item_state(item)

    def store_item_state(self, item):
        """Recursively store the state of an item and its children."""
        self.original_tree_state[item] = {
            'open': self.tree.item(item)['open'],
            'parent': self.tree.parent(item),
            'index': self.tree.index(item)
        }
        for child in self.tree.get_children(item):
            self.store_item_state(child)

    def restore_tree_state(self):
        """Restore the original expanded/collapsed state of all items."""
        if not self.original_tree_state:
            return

        # First, show all items in their original structure
        for item, state in self.original_tree_state.items():
            parent = state['parent']
            index = state['index']

            # Reattach the item to its original parent and position
            try:
                if parent:
                    children = list(self.tree.get_children(parent))
                    if index < len(children):
                        self.tree.move(item, parent, index)
                    else:
                        self.tree.reattach(item, parent, 'end')
                else:
                    self.tree.reattach(item, '', 'end')

                # Restore the open/closed state
                self.tree.item(item, open=state['open'])
            except:
                continue  # Skip if item no longer exists

        # Ensure all items are visible
        for item in self.tree.get_children():
            self.show_item_and_children(item)

    def hide_item_and_children(self, item):
        """Recursively hide an item and its children."""
        self.tree.detach(item)
        for child in self.tree.get_children(item):
            self.hide_item_and_children(child)

    def show_item_and_children(self, item):
        """Recursively show an item and its children."""
        self.tree.reattach(item, self.tree.parent(item), 'end')
        for child in self.tree.get_children(item):
            self.show_item_and_children(child)

    def show_item_and_parents(self, item):
        """Show an item and all its parent items up to the root."""
        parent = self.tree.parent(item)
        if parent:
            self.show_item_and_parents(parent)
            self.tree.reattach(parent, self.tree.parent(parent), 'end')
            self.tree.item(parent, open=True)
        self.tree.reattach(item, parent, 'end')

    def load_icon(self, path, size=(16, 16)):
        return ImageTk.PhotoImage(Image.open(path).resize(size, Image.LANCZOS))

    def toggle_folders(self):
        first_item = self.tree.get_children("")
        if not first_item:
            return
        if self.folders_expanded:
            self.collapse_all()
            self.toggle_icon = self.plus_icon
            self.folders_expanded = False
            self.toggle_tip.text = 'Open folders'
        else:
            self.expand_all()
            self.toggle_icon = self.minus_icon
            self.folders_expanded = True
            self.toggle_tip.text = 'Close folders'

        self.toggle_button_Close_Folders.config(image=self.toggle_icon)

    def expand_all(self):
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            self.expand_all_nodes(item)

    def expand_all_nodes(self, parent):
        for item in self.tree.get_children(parent):
            self.tree.item(item, open=True)
            self.expand_all_nodes(item)

    def collapse_all(self):
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            self.collapse_all_nodes(item)

    def collapse_all_nodes(self, parent):
        for item in self.tree.get_children(parent):
            self.tree.item(item, open=False)
            self.collapse_all_nodes(item)

    def open_settings(self):
        global Output_Folder_Path, Project_Order_By, Dir_FLP_Projects, Set_Output_Sub_Folder
        global Output_Sub_Folder_Name, Mouse_Scroll_Speed, FL_Studio_Path
        Settings_Info_Label_Size = 12

        if not self.settings_open:
            if hasattr(self, 'settings_frame'):
                self.settings_frame.destroy()
            # Hide main UI
            self.left_frame.pack_forget()
            self.right_frame.pack_forget()
            self.content_frame.pack_forget()
            self.toggle_button_Close_Folders.pack_forget()
            self.sync_button.pack_forget()

            # Change heading
            self.heading.config(text="Settings")

            # Show close button and update settings button
            self.close_button.pack(side=tk.RIGHT, padx=(0, 10))
            self.settings_button.config(text="Save Settings", image='')
            self.settings_open = True

            # Create the main settings container frame
            self.settings_frame = ttk.Frame(self.root, style='Settings.TFrame')
            self.settings_frame.pack(fill=tk.BOTH,
                                     expand=True,
                                     padx=20,
                                     pady=10)

            # Create a canvas and vertical scrollbar
            self.settings_canvas = tk.Canvas(self.settings_frame,
                                             highlightthickness=0,
                                             bg=Background_Color)
            self.settings_scrollbar = ttk.Scrollbar(
                self.settings_frame,
                orient="vertical",
                command=self.settings_canvas.yview)

            # Create the scrollable frame that will hold all settings widgets
            self.scrollable_settings_frame = ttk.Frame(self.settings_canvas,
                                                       style='Settings.TFrame')
            # Do NOT pack the scrollable frame; it's managed by the canvas
            self.scrollable_settings_frame.bind(
                "<Configure>", lambda e: self.settings_canvas.configure(
                    scrollregion=self.settings_canvas.bbox("all")))

            # Create window in canvas for scrollable frame
            self.settings_canvas.create_window(
                (0, 0),
                window=self.scrollable_settings_frame,
                anchor="nw",
                tags=("scroll_frame", ))
            # Add this binding to handle window resizing
            self.settings_canvas.bind("<Configure>", self._on_canvas_resize)

            self.settings_canvas.configure(
                yscrollcommand=self.settings_scrollbar.set,
                scrollregion=(0, 0, 0, 2000))

            # Pack the canvas and scrollbar
            self.settings_canvas.pack(side="left", fill="both", expand=True)
            self.settings_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))

            # Mouse wheel binding for scrolling
            self.settings_canvas.bind_all("<MouseWheel>",
                                          self._on_mousewheel_settings)

            #
            # General
            #
            self.general_header = ttk.Label(self.scrollable_settings_frame,
                                            text="General",
                                            font=(Font_Name, 18, "bold"))
            self.general_header.pack(anchor="w", padx=0, pady=(10, 5))

            # Output Folder Picker
            output_folder_frame = ttk.Frame(self.scrollable_settings_frame,
                                            style='Settings.TFrame')
            output_folder_frame.pack(fill=tk.X, pady=0)

            self.output_folder_label = ttk.Label(output_folder_frame,
                                                 text="Output Folder",
                                                 font=(Font_Name, 14),
                                                 style='Settings.TLabel')
            self.output_folder_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)

            self.output_folder_entry = ttk.Entry(output_folder_frame)
            self.output_folder_entry.pack(side=tk.LEFT,
                                          fill=tk.X,
                                          expand=True,
                                          padx=(0, 5))
            self.output_folder_entry.insert(0, Output_Folder_Path)

            self.browse_button = ttk.Button(output_folder_frame,
                                            text="Browse",
                                            command=self.browse_output_folder,
                                            bootstyle="info")
            self.browse_button.pack(side=tk.LEFT)
            self.output_folder_entry = ttk.Entry(output_folder_frame,
                                                 style='Settings.TEntry')

            self.output_folder_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text="This is where your mp3 songs will be exported to.",
                font=(Font_Name, Settings_Info_Label_Size),
                foreground="black")
            self.output_folder_info_label.pack(anchor="w",
                                               padx=20,
                                               pady=(2, 10))

            # FLP Projects Folder Picker (Multiple folders)
            flp_folder_frame = ttk.Frame(self.scrollable_settings_frame,
                                         style='Settings.TFrame')
            flp_folder_frame.pack(fill=tk.X, pady=0)

            self.flp_folder_label = ttk.Label(flp_folder_frame,
                                              text="FLP Projects Folders",
                                              font=(Font_Name, 14))
            self.flp_folder_label.pack(side=tk.LEFT, padx=(10, 0), pady=5)

            self.flp_folder_entry = ttk.Entry(flp_folder_frame)
            self.flp_folder_entry.pack(side=tk.LEFT,
                                       fill=tk.X,
                                       expand=True,
                                       padx=(0, 5))
            # Display existing folders separated by semicolons if they exist
            if hasattr(self, 'Dir_FLP_Projects'):
                self.flp_folder_entry.insert(0, "; ".join(Dir_FLP_Projects))

            self.browse_flp_button = ttk.Button(
                flp_folder_frame,
                text="Browse",
                command=self.browse_flp_folders,
                bootstyle="info")
            self.browse_flp_button.pack(side=tk.LEFT)

            # Add label underneath
            self.flp_folder_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text=
                ("This is where your FLP projects are, add the top folder.\n"
                 "Click Browse to add multiple folders.\n"
                 "Example - C:\\Users\\Kfoen\\Documents\\Image-Line\\FL Studio\\Projects\\FL 25 - projects"
                 ),
                font=(Font_Name, Settings_Info_Label_Size),
                foreground="black")
            self.flp_folder_info_label.pack(anchor="w", padx=20, pady=(2, 10))

            # Project Order selection
            order_frame = ttk.Frame(self.scrollable_settings_frame,
                                    style='Settings.TFrame')
            order_frame.pack(fill=tk.X, pady=0)

            self.order_label = ttk.Label(order_frame,
                                         text="Project Order",
                                         font=(Font_Name, 14),
                                         background=Background_Color)
            self.order_label.pack(side=tk.LEFT, padx=(10, 5))

            self.order_var = tk.StringVar(value=Project_Order_By)
            self.order_combobox = ttk.Combobox(
                order_frame,
                textvariable=self.order_var,
                values=["date", "name"],
                state="readonly",
                width=10,
                style="CustomCombobox.TCombobox")
            self.order_combobox.pack(side=tk.LEFT)
            self.order_combobox.configure(font=(Font_Name, 14))

            # Theme selection
            theme_frame = ttk.Frame(self.scrollable_settings_frame,
                                    style='Settings.TFrame')
            theme_frame.pack(fill=tk.X, pady=10)

            self.theme_label = ttk.Label(theme_frame,
                                         text="Theme",
                                         font=(Font_Name, 14))
            self.theme_label.pack(side=tk.LEFT, padx=(10, 10))

            self.theme_var = tk.StringVar(value="Default")  # Default selection
            self.theme_combobox = ttk.Combobox(theme_frame,
                                               textvariable=self.theme_var,
                                               values=THEME_NAMES,
                                               state="readonly",
                                               width=15,
                                               font=(Font_Name, 12))
            self.theme_combobox.pack(side=tk.LEFT)

            # Info label
            self.theme_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text=
                "Change the application's color scheme. Requires restart to apply.",
                font=(Font_Name, Settings_Info_Label_Size))
            self.theme_info_label.pack(anchor="w", padx=20, pady=(0, 10))

            #
            # Advanced
            #
            self.general_header = ttk.Label(self.scrollable_settings_frame,
                                            text="Advanced",
                                            font=(Font_Name, 18, "bold"))
            self.general_header.pack(anchor="w", padx=0, pady=(60, 5))

            # FL Studio Path Picker
            fl_studio_frame = ttk.Frame(self.scrollable_settings_frame,
                                        style='Settings.TFrame')
            fl_studio_frame.pack(fill=tk.X, pady=5)

            self.fl_studio_path_label = ttk.Label(fl_studio_frame,
                                                  text="FL Studio Path",
                                                  font=(Font_Name, 14))
            self.fl_studio_path_label.pack(side=tk.LEFT, padx=(10, 5))

            self.fl_studio_path_entry = ttk.Entry(fl_studio_frame)
            self.fl_studio_path_entry.pack(side=tk.LEFT,
                                           fill=tk.X,
                                           expand=True,
                                           padx=(0, 5))
            # Set current path if it exists
            if hasattr(self, 'FL_Studio_Path') and self.FL_Studio_Path:
                self.fl_studio_path_entry.insert(0, self.FL_Studio_Path)

            self.browse_fl_studio_button = ttk.Button(
                fl_studio_frame,
                text="Browse",
                command=self.browse_fl_studio_path,
                bootstyle="info")
            self.browse_fl_studio_button.pack(side=tk.LEFT)

            # Info label
            self.fl_studio_path_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text=
                ("Path to your FL Studio installation folder.\nEnsure this is the correct path as you will not be able to export if the path is incorrect.\nExample - C:\\Program Files\\Image-Line\\FL Studio 21"
                 ),
                font=(Font_Name, Settings_Info_Label_Size))
            self.fl_studio_path_info_label.pack(anchor="w",
                                                padx=20,
                                                pady=(0, 10))

            # Processor Type Dropdown
            processor_frame = ttk.Frame(self.scrollable_settings_frame,
                                        style='Settings.TFrame')
            processor_frame.pack(fill=tk.X, pady=5)

            self.processor_label = ttk.Label(processor_frame,
                                             text="Processor Type",
                                             font=(Font_Name, 14))
            self.processor_label.pack(side=tk.LEFT, padx=(10, 10))

            # Create a StringVar to store the selected value
            self.processor_type = tk.StringVar(
                value="FL64.exe")  # Default value

            # Create the Combobox dropdown
            self.processor_dropdown = ttk.Combobox(
                processor_frame,
                textvariable=self.processor_type,
                values=["FL64.exe", "FL.exe"],
                font=(Font_Name, 14),
                state="readonly",
                width=15)
            self.processor_dropdown.pack(side=tk.LEFT)

            # Info label
            self.processor_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text="Select FL64.exe (64-bit) or FL.exe (32-bit)",
                font=(Font_Name, 12))
            self.processor_info_label.pack(anchor="w", padx=20, pady=(0, 10))

            # Output Subfolder Toggle and Entry
            subfolder_frame = ttk.Frame(self.scrollable_settings_frame)
            subfolder_frame.pack(fill=tk.X, pady=5)
            style.configure('Large.TCheckbutton',
                            font=('Segoe UI', 14))  # <<< NEW

            # Launch at Startup Toggle
            startup_frame = ttk.Frame(self.scrollable_settings_frame,
                                      style='Settings.TFrame')
            startup_frame.pack(fill=tk.X, pady=10)

            self.startup_label = ttk.Label(
                startup_frame,
                text="Launch application at system startup",
                font=(Font_Name, 14))
            self.startup_label.pack(side=tk.LEFT, padx=(10, 10))

            self.startup_var = tk.BooleanVar(value=self.check_startup_status())
            self.startup_toggle = ttk.Checkbutton(
                startup_frame,
                variable=self.startup_var,
                #   bootstyle="round-toggle",
                style='Settings.TCheckbutton',
                command=self.toggle_startup)
            self.startup_toggle.pack(side=tk.LEFT, padx=(0, 40))

            # Enable Output Subfolder Toggle
            subfolder_toggle_frame = ttk.Frame(self.scrollable_settings_frame,
                                               style='Settings.TFrame')
            subfolder_toggle_frame.pack(fill=tk.X, pady=10, padx=0)

            self.enable_subfolder_label = ttk.Label(
                subfolder_toggle_frame,
                text="Enable output subfolder",
                font=(Font_Name, 14),
                style='Settings.TLabel')
            self.enable_subfolder_label.pack(side=tk.LEFT, padx=(10, 20))

            self.subfolder_toggle_var = tk.BooleanVar(
                value=Set_Output_Sub_Folder)
            self.subfolder_toggle = ttk.Checkbutton(
                subfolder_toggle_frame,
                variable=self.subfolder_toggle_var,
                bootstyle="round-toggle",
                command=self.toggle_subfolder_entry,
                style='Settings.TCheckbutton')
            self.subfolder_toggle.pack(side=tk.LEFT)
            self.subfolder_toggle.pack(side=tk.LEFT, padx=(0, 10))
            # Info label
            self.subfolder_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text=
                ("Creates a subfolder in your output directory, to maintain a more organized output directory.\nFor example an album name."
                 ),
                font=(Font_Name, Settings_Info_Label_Size))
            self.subfolder_info_label.pack(anchor="w", padx=20, pady=(0, 10))

            # Mouse Scroll Speed Dropdown
            scroll_frame = ttk.Frame(self.scrollable_settings_frame,
                                     style='Settings.TFrame')
            scroll_frame.pack(fill=tk.X, pady=5)

            self.scroll_speed_label = ttk.Label(
                scroll_frame,
                text="Mouse Scroll Speed in Projects:",
                font=(Font_Name, 14))
            self.scroll_speed_label.pack(side=tk.LEFT, padx=(10, 10))

            SCROLL_SPEED_MAPPING = {
                1: 7,  # Slow
                2: 10,  # Medium (default)
                3: 15,  # Fast
                4: 19  # Very fast
            }

            # Find which key has our current value (reverse lookup)
            current_key = next(
                (k for k, v in SCROLL_SPEED_MAPPING.items()
                 if v == Mouse_Scroll_Speed),
                2  # Default to medium if not found
            )

            self.scroll_speed_var = tk.IntVar(value=current_key)
            self.scroll_combobox = ttk.Combobox(
                scroll_frame,
                textvariable=self.scroll_speed_var,
                values=list(SCROLL_SPEED_MAPPING.keys()),
                state="readonly",
                width=5,
                font=(Font_Name, 14))
            self.scroll_combobox.pack(side=tk.LEFT)

            # Info label showing speed descriptions
            self.scroll_info_label = ttk.Label(
                self.scrollable_settings_frame,
                text="1 Slow\n2 Medium\n3 Fast\n4 Very Fast",
                font=(Font_Name, 12))
            self.scroll_info_label.pack(anchor="w", padx=20, pady=(0, 10))

            #
            # ABOUT
            #

            # About Section
            self.about_header = ttk.Label(self.scrollable_settings_frame,
                                          text="About",
                                          font=(Font_Name, 18, "bold"))
            self.about_header.pack(anchor="w", padx=30, pady=(60, 5))

            # Version Info
            version_frame = ttk.Frame(self.scrollable_settings_frame,
                                      style='Settings.TFrame')
            version_frame.pack(fill=tk.X, pady=(0, 10))

            self.version_label = ttk.Label(version_frame,
                                           text="Version 1.1",
                                           foreground="black",
                                           font=(Font_Name, 14))
            self.version_label.pack(
                side=tk.LEFT,
                padx=(30, 10),
            )

            # Warning Note
            self.warning_note = ttk.Label(
                self.scrollable_settings_frame,
                text=
                "Note: FL Studio must be closed before exporting song.\nMake sure to save your project.\nClicking export will automatically close FL Studio.\n\nIf your project has a popup, (unlicensed vst, audio missing) we recommend buying the vst as FL intends, or replacing the missing audio.\nThe project will continue to export once you click ok, or remove the popup." \
                "\n\nBackup projects are not shown, in order to reduce duplicates.",
                font=(Font_Name, 15),
                foreground="black",
                wraplength=1000,
                justify=tk.LEFT)
            self.warning_note.pack(anchor="w", padx=20,
                                   pady=(0, 60))  # Added padding at bottom
            self.settings_canvas.configure(
                scrollregion=self.settings_canvas.bbox("all"))

        else:
            # Save output path
            new_path = self.output_folder_entry.get().strip()
            if not os.path.isdir(new_path):
                print(
                    "Error", "The specified directory does not exist.")
                return
            Output_Folder_Path = new_path

            # Save FLP projects folders
            flp_folders = self.flp_folder_entry.get().strip()
            if flp_folders:
                Dir_FLP_Projects = [
                    f.strip() for f in flp_folders.split(";") if f.strip()
                ]
                # Validate each folder
                for folder in Dir_FLP_Projects:
                    if not os.path.isdir(folder):
                        messagebox.showerror(
                            "Error",
                            f"The specified FLP directory does not exist: {folder}"
                        )
                        return

            # Save project order
            Project_Order_By = self.order_var.get()

            # Handle startup setting
            if self.startup_var.get():
                self.add_to_startup()
            else:
                self.remove_from_startup()

            # Save subfolder settings
            Set_Output_Sub_Folder = self.subfolder_toggle_var.get()
            if Set_Output_Sub_Folder:
                subfolder_name = self.subfolder_entry.get().strip()
                if not subfolder_name:
                    # Keep code, as if removd, it disbales writing in output sub folder
                    return
                Output_Sub_Folder_Name = subfolder_name

            # Save mouse scroll speed
            selected_key = self.scroll_speed_var.get()
            Mouse_Scroll_Speed = SCROLL_SPEED_MAPPING.get(
                selected_key, 10)  # Default to medium if invalid

            # Save FL Studio path
            fl_studio_path = self.fl_studio_path_entry.get().strip()
            if fl_studio_path:  # Only validate if path is provided
                if not os.path.isdir(fl_studio_path):
                    messagebox.showerror(
                        "Error",
                        "The specified FL Studio directory does not exist.")
                    return
                FL_Studio_Path = fl_studio_path

            # Destroy settings UI
            self.settings_frame.destroy()
            self.settings_open = False

            # Unbind mouse wheel
            self.settings_canvas.unbind_all("<MouseWheel>")

            self.restore_header_and_ui()

    def browse_flp_folders(self):
        """Open a dialog to select multiple FLP project folders"""
        folders = filedialog.askdirectory(mustexist=True,
                                          title="Select FLP Project Folders")
        if folders:
            # Get current folders from the entry
            current_folders = self.flp_folder_entry.get()
            if current_folders:
                # Append new folder to existing ones, separated by semicolon
                updated_folders = f"{current_folders}; {folders}"
            else:
                updated_folders = folders
            self.flp_folder_entry.delete(0, tk.END)
            self.flp_folder_entry.insert(0, updated_folders)

    def browse_output_folder(self):
        global Output_Folder_Path
        folder_selected = filedialog.askdirectory(
            initialdir=Output_Folder_Path)
        if folder_selected:
            self.output_folder_entry.delete(0, tk.END)
            self.output_folder_entry.insert(0, folder_selected)

    def close_settings_without_saving(self):
        # Close settings without saving
        self.settings_frame.destroy()
        self.settings_open = False
        self.settings_button.config(text="Settings", image=self.settings_icon)
        self.close_button.pack_forget()

        # Unbind mouse wheel
        self.settings_canvas.unbind_all("<MouseWheel>")

        self.restore_header_and_ui()

    def restore_header_and_ui(self):
        # Restore header and UI
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.output_music_folder_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.heading.config(text=f"🎵 {Application_Name}")
        self.settings_button.config(text="Settings", image=self.settings_icon)
        self.close_button.pack_forget()
        self.sync_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))

    def on_enter_key(self, event):
        selected_items = self.tree.selection()
        for item_id in selected_items:
            if item_id in self.path_map:
                file_path = self.path_map[item_id]
                if file_path in self.selected_files:
                    self.selected_files.remove(file_path)
                    self.tree.item(item_id, tags=())
                else:
                    self.selected_files.add(file_path)
                    self.tree.item(item_id, tags=("selected", ))
        self.anchor_item = None
        self.refresh_cart()

    def populate_tree(self, parent_paths, parent_node=""):
        if isinstance(parent_paths, str):
            parent_paths = [parent_paths]

        # First pass: Create top-level nodes for each root directory
        for path in parent_paths:
            root_name = os.path.basename(path)
            root_node = self.tree.insert(parent_node,
                                         "end",
                                         text=root_name,
                                         open=True)
            self.all_items[root_node] = root_name
            self.scan_directory(path, root_node)

        self.store_tree_state()

    def scan_directory(self, current_path, parent_node):
        """Scans directory and adds items to tree with proper ordering"""
        try:
            entries = os.listdir(current_path)
            dirs = []
            files = []

            # Separate directories and files
            for entry in entries:
                full_path = os.path.join(current_path, entry)
                if "Backup" in full_path.split(os.sep):
                    continue

                if os.path.isdir(full_path):
                    # Check if directory contains FLP files
                    has_flp = False
                    for root, dirs_walk, files_walk in os.walk(full_path):
                        if any(f.lower().endswith('.flp') for f in files_walk):
                            has_flp = True
                            break
                    if has_flp:
                        dirs.append((entry, full_path))
                elif entry.lower().endswith(".flp"):
                    files.append((entry, full_path))

            # Always show subfolders first
            # Ensure we pass empty list if no dirs
            sorted_dirs = self._sort_items(dirs or [], current_path)
            for item in sorted_dirs:
                if len(item) >= 2:  # Ensure we have at least 2 elements
                    entry, full_path = item[0], item[1]
                    node = self.tree.insert(parent_node,
                                            "end",
                                            text=entry,
                                            open=True)
                    self.all_items[node] = entry
                    self.scan_directory(full_path, node)

            # Then show files
            # Ensure we pass empty list if no files
            sorted_files = self._sort_items(files or [], current_path)
            for item in sorted_files:
                if len(item) >= 2:  # Ensure we have at least 2 elements
                    entry, full_path = item[0], item[1]
                    clean_name = re.sub(r"\.flp$",
                                        "",
                                        entry,
                                        flags=re.IGNORECASE)
                    item_id = self.tree.insert(parent_node,
                                               "end",
                                               text=clean_name,
                                               values=(full_path, ))
                    self.all_items[item_id] = clean_name
                    self.path_map[item_id] = full_path

        except PermissionError:
            pass

    def _sort_items(self, items, parent_path):
        """Sorts items based on Project_Order_By setting"""
        if not items:  # Return empty list if no items
            return []

        if Project_Order_By == "date":
            # Sort by modification date (newest first)
            def get_mtime(item):
                if len(item) >= 2:  # Ensure we have at least 2 elements
                    item_path = os.path.join(parent_path, item[0])
                    try:
                        return os.path.getmtime(item_path)
                    except (OSError, AttributeError):
                        return 0  # Default value if can't get mtime
                return 0

            return sorted(items, key=get_mtime, reverse=True)
        else:
            # Default: sort by name (case-insensitive)
            return sorted(items,
                          key=lambda x: x[0].lower() if len(x) >= 1 else "")

    def on_tree_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "tree":
            return
        item_id = self.tree.identify_row(event.y)
        if not item_id or item_id not in self.path_map:
            return
        file_path = self.path_map[item_id]
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self.tree.item(item_id, tags=())
        else:
            if event.state & 0x0001:
                self.select_range(item_id)
            elif event.state & 0x0004:
                self.toggle_select(item_id)
            else:
                self.selected_files.add(file_path)
                self.tree.item(item_id, tags=("selected", ))
        self.anchor_item = item_id
        self.refresh_cart()

    def select_range(self, new_item_id):
        if self.last_selected_item is None:
            self.selected_files.add(self.path_map[new_item_id])
            self.tree.item(new_item_id, tags=("selected", ))
            self.last_selected_item = new_item_id
            return
        start_idx = self.tree.index(self.last_selected_item)
        end_idx = self.tree.index(new_item_id)
        for idx in range(min(start_idx, end_idx), max(start_idx, end_idx) + 1):
            item_id = self.tree.get_children()[idx]
            if item_id in self.path_map:
                self.selected_files.add(self.path_map[item_id])
                self.tree.item(item_id, tags=("selected", ))
        self.last_selected_item = new_item_id

    def toggle_select(self, item_id):
        file_path = self.path_map[item_id]
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self.tree.item(item_id, tags=())
        else:
            self.selected_files.add(file_path)
            self.tree.item(item_id, tags=("selected", ))
        self.last_selected_item = item_id

    def on_cart_double_click(self, event):
        selection = self.cart_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        name = self.cart_listbox.get(index)
        file_to_remove = None
        for path in self.selected_files:
            if re.sub(r"\.flp$",
                      "",
                      os.path.basename(path),
                      flags=re.IGNORECASE) == name:
                file_to_remove = path
                break
        if file_to_remove:
            self.selected_files.remove(file_to_remove)
            for item_id, path in self.path_map.items():
                if path == file_to_remove:
                    self.tree.item(item_id, tags=())
                    break
            self.refresh_cart()

    def refresh_cart(self):
        self.cart_listbox.delete(0, tk.END)
        for path in sorted(self.selected_files):
            name = re.sub(r"\.flp$",
                          "",
                          os.path.basename(path),
                          flags=re.IGNORECASE)
            self.cart_listbox.insert(tk.END, name)

    def export_selected(self):
        # Clear the status completely and force GUI update
        self.status_label.config(text="")
        self.status_label.update()
        self.root.update_idletasks()  # Force complete GUI refresh

        if not self.selected_files:
            self.status_label.config(text="No files selected.",
                                     bootstyle="primary")
            self.status_label.update()
            return

        total = len(self.selected_files)
        try:
            # Set exporting message and force display
            self.status_label.config(text="Exporting...", bootstyle="warning")
            self.status_label.update()
            self.root.update_idletasks()  # Force complete GUI refresh

            for idx, path in enumerate(self.selected_files, 1):
                print(f"[{idx}/{total}] Exporting {os.path.basename(path)}")
                export_flp_to_mp3(path)

            # Clear before showing success message
            self.status_label.config(text="")
            self.status_label.update()

            Exported_project_label = "project" if total == 1 else "projects"
            self.status_label.config(
                text=f"{total} {Exported_project_label} exported.",
                bootstyle="success")
            self.status_label.update()

        except Exception as e:
            # Clear completely before error message
            self.status_label.config(text="")
            self.status_label.update()
            self.status_label.config(text=f"Export failed: {str(e)}",
                                     bootstyle="danger")
            self.status_label.update()

    def clear_selection(self):
        for item_id in self.path_map:
            self.tree.item(item_id, open=False, tags=())
        self.selected_files.clear()
        self.cart_listbox.delete(0, tk.END)
        self.status_label.config(text="Selection cleared.",
                                 bootstyle="primary")
        self.anchor_item = None

    def add_recent_projects(self):
        today = datetime.date.today()
        today_str = today.strftime("%d-%m-%Y")
        file_paths = get_file_paths(Dir_FLP_Projects)

        # First count all today's files (regardless of selection status)
        total_today_files = 0
        for modified_date in file_paths.values():
            if datetime.datetime.fromtimestamp(modified_date).strftime(
                    "%d-%m-%Y") == today_str:
                total_today_files += 1

        # Now count how many were actually added (not previously selected)
        added = 0
        for file_path, modified_date in file_paths.items():
            if datetime.datetime.fromtimestamp(modified_date).strftime(
                    "%d-%m-%Y") == today_str:
                if file_path not in self.selected_files:
                    self.selected_files.add(file_path)
                    for item_id, path in self.path_map.items():
                        if path == file_path:
                            self.tree.item(item_id, tags=("selected", ))
                            break
                    added += 1

        self.refresh_cart()

        if total_today_files == 0:
            self.status_label.config(text="No files modified today.",
                                     bootstyle="primary")
        else:
            if added > 0:
                # Show how many new files were added
                Recent_Project_Label = "project" if added == 1 else "projects"
                self.status_label.config(
                    text=f"{added}\nrecent {Recent_Project_Label} added.",
                    bootstyle="primary")
            else:
                # Show that all today's files were already selected
                Recent_Project_Label = "project" if total_today_files == 1 else "projects"
                #self.status_label.config(text=f"All {total_today_files} recent {Recent_Project_Label} already selected.", bootstyle="info")
                self.status_label.config(
                    text=
                    f"{total_today_files} recent {Recent_Project_Label} added.",
                    bootstyle="primary")

    def on_mousewheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.tree.yview_scroll(Mouse_Scroll_Speed * delta, "units")

    # Right click opens the file
    def on_right_click(self, event):
        """Handle right-click to show context menu"""
        item_id = self.tree.identify_row(event.y)
        self.context_item = item_id  # Store the clicked item

        if item_id:
            # Create context menu
            self.context_menu = tk.Menu(self.root, tearoff=0)

            # For FLP files (items in path_map)
            if item_id in self.path_map:
                self.context_menu.add_command(label="Open File",
                                              command=self.open_selected_file)
                self.context_menu.add_command(
                    label="Open Folder", command=self.open_containing_folder)
            # For folders (items not in path_map)
            else:
                self.context_menu.add_command(
                    label="Open Folder",
                    command=lambda: self.open_folder(item_id))

            # Show menu at cursor position if we added any items
            if self.context_menu.index(tk.END) is not None:
                self.context_menu.post(event.x_root, event.y_root)

    def open_folder(self, item_id):
        """Open the selected folder in File Explorer"""
        try:
            # Check if this is a top-level folder (direct child of tree root)
            if not self.tree.parent(item_id):  # Top-level item
                # Get the folder name
                folder_name = self.tree.item(item_id, 'text')

                # Find matching root directory
                for dir_path in Dir_FLP_Projects:
                    if os.path.basename(dir_path) == folder_name:
                        if os.path.isdir(dir_path):
                            os.startfile(dir_path)
                            return
                        else:
                            messagebox.showerror("Error",
                                                 "Folder path does not exist")
                            return

                messagebox.showerror("Error",
                                     "Could not find matching root directory")
                return

            # For nested folders (original logic)
            path_parts = []
            current_id = item_id

            # Walk up the tree to build the full path
            while current_id:
                text = self.tree.item(current_id, 'text')
                path_parts.insert(0, text)
                current_id = self.tree.parent(current_id)

            # Find which root directory this belongs to
            root_node = self.tree.parent(item_id)
            while self.tree.parent(root_node):  # Walk up to top-level node
                root_node = self.tree.parent(root_node)

            root_text = self.tree.item(root_node, 'text')

            # Find the matching root directory path
            root_path = None
            for dir_path in Dir_FLP_Projects:
                if os.path.basename(dir_path) == root_text:
                    root_path = dir_path
                    break

            if root_path:
                # Reconstruct the full folder path
                full_path = os.path.join(root_path, *path_parts[1:])
                if os.path.isdir(full_path):
                    os.startfile(full_path)
                else:
                    messagebox.showerror("Error", "Folder path does not exist")
            else:
                messagebox.showerror("Error",
                                     "Could not determine folder path")

        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {str(e)}")
        finally:
            if hasattr(self, 'context_menu'):
                self.context_menu.destroy()

    def open_selected_file(self):
        """Open the selected file directly"""
        if hasattr(self,
                   'context_item') and self.context_item in self.path_map:
            file_path = self.path_map[self.context_item]
            try:
                os.startfile(file_path)
                #self.status_label.config(text="File opened successfully", bootstyle="success")
            except Exception as e:
                #self.status_label.config( text=f"Error opening file: {str(e)}", bootstyle="danger")
                pass
            finally:
                self.context_menu.destroy()

    def open_containing_folder(self):
        """Open the folder containing the selected file"""
        if hasattr(self,
                   'context_item') and self.context_item in self.path_map:
            file_path = self.path_map[self.context_item]
            folder_path = os.path.dirname(file_path)

            try:
                os.startfile(folder_path)
                #self.status_label.config( text="Folder opened successfully", bootstyle="success")
            except Exception as e:
                #self.status_label.config(text=f"Error opening folder: {str(e)}", bootstyle="danger")
                pass
            finally:
                self.context_menu.destroy()

    def sync_projects(self):
        """Sync and update the project tree while preserving folder states"""
        try:
            # Store current selection
            current_selection = set(self.selected_files)

            # Visual refresh - flash the frames
            self.flash_refresh()

            # Clear and repopulate the tree
            self.tree.delete(*self.tree.get_children())
            self.path_map.clear()
            self.all_items.clear()
            self.selected_files.clear()
            self.cart_listbox.delete(0, tk.END)
            self.populate_tree(Dir_FLP_Projects)

            # Force expand all folders using existing toggle mechanism
            if not self.folders_expanded:
                self.toggle_folders()  # Use existing toggle logic

            self.expand_all()  # Ensure all nodes are expanded
            self.toggle_button_Close_Folders.config(image=self.minus_icon)
            self.toggle_tip.text = 'Close folders'

            # Restore selection
            for path in current_selection:
                for item_id, item_path in self.path_map.items():
                    if path == item_path:
                        self.selected_files.add(path)
                        self.tree.item(item_id, tags=("selected", ))

            self.refresh_cart()
            self.status_label.config(text="Project tree synced",
                                     bootstyle="primary")

        except Exception as e:
            self.status_label.config(text=f"Sync failed: {str(e)}",
                                     bootstyle="danger")

    def flash_refresh(self):
        """Visual effect to show refresh is happening"""
        # Temporarily hide frames
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()

        # Update the UI immediately
        self.root.update_idletasks()

        # Brief delay
        self.root.after(5, self._show_frames_after_flash)

    def _show_frames_after_flash(self):
        """Shows frames again after flash effect"""
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        ###

    def toggle_startup(self):
        """Handle the startup toggle button"""
        if self.startup_var.get():
            self.add_to_startup()
        else:
            self.remove_from_startup()

    def add_to_startup(self):
        """Add the program to Windows startup"""
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle (pyinstaller)
            app_path = sys.executable
        else:
            app_path = os.path.abspath(__file__)

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Run',
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "FLPManager", 0, winreg.REG_SZ, app_path)
        winreg.CloseKey(key)

    def remove_from_startup(self):
        """Remove the program from Windows startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run', 0,
                winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "FLPManager")
            winreg.CloseKey(key)
        except WindowsError:
            pass  # Key didn't exist, which is fine

    def check_startup_status(self):
        """Check if the program is in Windows startup"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r'Software\Microsoft\Windows\CurrentVersion\Run', 0,
                winreg.KEY_READ)
            winreg.QueryValueEx(key, "FLPManager")
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    def browse_fl_studio_path(self):
        """Open a dialog to select FL Studio installation folder"""
        path = filedialog.askdirectory(
            mustexist=True,
            title="Select FL Studio Installation Folder",
            initialdir="C:\\Program Files"  # Common installation location
        )
        if path:
            self.fl_studio_path_entry.delete(0, tk.END)
            self.fl_studio_path_entry.insert(0, path)

    def toggle_subfolder_entry(self):
        """Enable/disable the subfolder entry based on toggle state"""
        if self.subfolder_toggle_var.get():
            self.subfolder_entry.config(state=tk.NORMAL)
        else:
            self.subfolder_entry.config(state=tk.DISABLED)

    def apply_scroll_speed(self):
        """Apply the selected scroll speed to the application"""
        if hasattr(self, 'canvas'):  # If you have a canvas widget
            self.canvas.configure(yscrollincrement=Mouse_Scroll_Speed)
        if hasattr(self, 'text_widget'):  # If you have text widgets
            self.text_widget.configure(yscrollincrement=Mouse_Scroll_Speed)
        # Add other widgets that need scroll speed adjustment

    def open_first_flp_folder(self):
        """Open the first FLP folder in File Explorer"""
        if Dir_FLP_Projects and len(Dir_FLP_Projects) > 0:
            first_folder = Dir_FLP_Projects[0]
            if os.path.isdir(first_folder):
                try:
                    os.startfile(first_folder)
                except Exception as e:
                   print("Error",
                                         f"Could not open folder: {str(e)}")
            else:
               print(
                    "Error", "The specified FLP directory does not exist")
        else:
            print("Error", "No FLP folders are set in settings")

    def _on_mousewheel_settings(self, event):
        """Handle mouse wheel scrolling for settings panel"""
        if event.delta:
            self.settings_canvas.yview_scroll(int(-1 * (event.delta / 120)),
                                              "units")
        else:
            if event.num == 5:
                self.settings_canvas.yview_scroll(1, "unit")
            elif event.num == 4:
                self.settings_canvas.yview_scroll(-1, "unit")

    def reset_anchor(self, event=None):
        """Reset anchor when keys are released"""
        self.anchor_item = None

    def get_visible_tree_items(self):
        """Get all visible items in treeview in display order (files + folders)"""

        def _get_items(parent=''):
            items = []
            for item in self.tree.get_children(parent):
                items.append(item)
                if self.tree.item(item, 'open'):
                    items.extend(_get_items(item))
            return items

        return _get_items()

    def select_range(self, new_item_id):
        """Selects items between last_selected_item and new_item_id based on visible order."""
        if self.last_selected_item is None:
            if new_item_id in self.path_map:
                self.selected_files.add(self.path_map[new_item_id])
                self.tree.item(new_item_id, tags=("selected", ))
                self.last_selected_item = new_item_id
            return

        visible_items = self.get_visible_items()
        try:
            start_idx = visible_items.index(self.last_selected_item)
            end_idx = visible_items.index(new_item_id)
        except ValueError:
            return  # One of the items is not visible

        for idx in range(min(start_idx, end_idx), max(start_idx, end_idx) + 1):
            item_id = visible_items[idx]
            if item_id in self.path_map:
                self.selected_files.add(self.path_map[item_id])
                self.tree.item(item_id, tags=("selected", ))

    def on_ctrl_shift_arrow(self, event):
        """Handle extended multi-selection with arrow keys"""
        direction = -1 if event.keysym == "Up" else 1
        all_items = self.get_visible_tree_items()

        try:
            current_index = all_items.index(self.tree.focus())
        except ValueError:
            current_index = 0

        # Find next valid file item
        new_item, new_index = self.find_next_file(current_index, direction)
        if not new_item:
            return "break"

        # Set initial anchor if none exists
        if not self.anchor_item or self.last_direction != direction:
            self.anchor_item = self.tree.focus() if self.tree.focus(
            ) in self.path_map else new_item
            self.last_direction = direction

        # Update selection range
        try:
            anchor_index = all_items.index(self.anchor_item)
        except ValueError:
            anchor_index = new_index

        start = min(anchor_index, new_index)
        end = max(anchor_index, new_index)
        selected_items = [
            all_items[i] for i in range(start, end + 1)
            if all_items[i] in self.path_map
        ]

        # Update UI state
        self.tree.focus(new_item)
        self.tree.see(new_item)
        for item in selected_items:
            self.selected_files.add(self.path_map[item])
            self.tree.item(item, tags=("selected", ))

        self.refresh_cart()
        return "break"

    def get_range_items(self, start_item, end_item):
        """Get items between two points in visible items list"""
        visible = self.get_visible_items()
        try:
            start_idx = visible.index(start_item)
            end_idx = visible.index(end_item)
        except ValueError:
            return []

        step = 1 if start_idx <= end_idx else -1
        return [visible[i] for i in range(start_idx, end_idx + step, step)]

    def on_key_release(self, event):
        """Reset anchor when control/shift keys are released"""
        if event.keysym in ('Control_L', 'Control_R', 'Shift_L', 'Shift_R'):
            self.anchor_item = None
            self.last_direction = None

    def find_next_file(self, start_index, direction):
        """Find next selectable file in given direction"""
        all_items = self.get_visible_tree_items()
        index = start_index + direction

        while 0 <= index < len(all_items):
            item = all_items[index]
            if item in self.path_map:
                return item, index
            index += direction
        return None, index

    # Add this method to handle canvas resizing
    def _on_canvas_resize(self, event):
        canvas_width = event.width
        self.settings_canvas.itemconfig("scroll_frame", width=canvas_width)

    def apply_theme(self, theme_name):
        """Apply the selected theme"""
        # Map your theme names to actual color values
        theme_colors = {
            "Dark Mode": {
                "bg": "#2d2d2d",
                "fg": "#ffffff",
                "highlight": "#3a7ebf"
            },
            "Cherry": {
                "bg": "#3a0f0f",
                "fg": "#ffcccc",
                "highlight": "#ff4d4d"
            },
            "Sky Blue": {
                "bg": "#e6f2ff",
                "fg": "#003366",
                "highlight": "#3399ff"
            },
            "Default": {
                "bg": "#f5f5f5",
                "fg": "#000000",
                "highlight": "#3498db"
            },
            "FL Skin": {
                "bg": "#2c3e50",
                "fg": "#f39c12",
                "highlight": "#e74c3c"
            },
            "Barbie": {
                "bg": "#ffccff",
                "fg": "#cc0099",
                "highlight": "#ff66b3"
            },
            "Forest Green": {
                "bg": "#0a2e0a",
                "fg": "#a3e4a3",
                "highlight": "#2ecc71"
            },
            "Brazil Tan": {
                "bg": "#f5e6d3",
                "fg": "#5c3a21",
                "highlight": "#d4a76a"
            },
            "Purple Rain": {
                "bg": "#AA336A",
                "fg": "#E6E6FA",
                "highlight": "#DA70D6"
            }
        }

        colors = theme_colors.get(theme_name, theme_colors["Default"])

        # Apply colors to main elements
        self.root.config(bg=colors["bg"])
        style.configure('.', background=colors["bg"], foreground=colors["fg"])
        style.configure('TLabel',
                        background=colors["bg"],
                        foreground=colors["fg"])
        style.configure('TFrame', background=colors["bg"])
        style.configure('TButton', background=colors["highlight"])

        # Update specific widgets
        self.top_bar.config(bg=colors["bg"])
        self.content_frame.config(bg=colors["bg"])
        self.left_frame.config(bg=colors["bg"])
        self.right_frame.config(bg=colors["bg"])

        # Update treeview colors
        style.configure("Custom.Treeview",
                        background=colors["bg"],
                        fieldbackground=colors["bg"],
                        foreground=colors["fg"])

        # Force update all widgets
        self.root.update_idletasks()


# === START APP ===
if __name__ == "__main__":
    style = Style("pulse" if USE_DARK_MODE else "flatly")
    root = style.master
    app = FLPExporterUI(root)
    root.mainloop()
