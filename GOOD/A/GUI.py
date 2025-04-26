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




global Output_Folder_Path
# === CONFIG ===
USE_DARK_MODE = False
Dir_FLP_Projects = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
#Dir_FLP_Projects = r"C:\Users\foendoe.kevin\Documents\findusic - FLP Input"
Output_Folder_Path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"


Search_Placeholder_Text = "Search Projects"
Set_Output_Sub_Folder = True
Output_Sub_Folder_Name = ""
Output_Audio_Format = "Emp3"
Mouse_Scroll_Speed = 7
Application_Name = "Multi FLP to MP3"
# Emp3,ogg,wav
#ogg does not work in powershell, FL might have disabled

# ---
# Colors
Selected_Project_Background_Color = "#34b1eb"
Selected_Project_Text_Color = "black"
Top_Title_Color ="black"
Search_Placeholder_Text_Color = "black"
Project_Color_Tree ="white"
# ---

def get_file_paths(root_directory):
    file_paths = {}
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
        os.system("taskkill /f /im FL.exe")    # For 32-bit version

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
        self.root.geometry("600x600+30+20")
        self.root.resizable(False, False)
        self.root.title(Application_Name)
        transparent_icon = tk.PhotoImage(width=1, height=1)
        self.root.iconbitmap(r"Media/icons/FL21 - Icon.ico")
        Background_Color = "white"
        self.root.configure(bg=Background_Color)
        self.folders_expanded = True
        self.settings_open = False
        style = ttk.Style()
        
        # Create top bar frame first
        self.top_bar = ttk.Frame(self.root)
        self.top_bar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        

        # Add heading to the top bar frame (left side)
        self.heading = ttk.Label(self.top_bar, text=f"🎵 {Application_Name}",
                                 font=("Segoe UI", 16, "bold"), bootstyle="info", foreground=Top_Title_Color)
        self.heading.pack(side=tk.LEFT, pady=0)

        self.download_icon = self.load_icon("Media/Icons/download.png")
        self.plus_icon = self.load_icon("Media/Icons/plus.png")
        self.minus_icon = self.load_icon("Media/Icons/minus.png")
        self.clear_icon = self.load_icon("Media/Icons/clear.png")
        self.recent_icon = self.load_icon("Media/Icons/recent.png")
        self.settings_icon = self.load_icon("Media/Icons/settings.png")
        self.music_folder_icon = self.load_icon("Media/Icons/musical-note.png")
        

        self.selected_files = set()
        self.path_map = {}
        self.last_selected_item = None
        self.all_items = {}
        self.original_tree_state = {}

        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.left_frame = ttk.Frame(content_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add search frame
        search_frame = ttk.Frame(self.left_frame, borderwidth=2, relief='solid')
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        style = ttk.Style()
        style.configure("Search.TEntry", relief="flat")

        self.search_entry = ttk.Entry(search_frame, style="Search.TEntry")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 0))

        # Output Sub Folder
        if Set_Output_Sub_Folder:
            self.subfolder_frame = ttk.Frame(search_frame)
            self.subfolder_frame.pack(side=tk.LEFT, fill=tk.X, padx=(0, 0))

            self.subfolder_label = ttk.Label(
                self.subfolder_frame, text="Output Subfolder:")
            self.subfolder_label.pack(side=tk.LEFT, padx=(5, 2))

            self.subfolder_entry = ttk.Entry(self.subfolder_frame, width=15)
            self.subfolder_entry.pack(side=tk.LEFT, fill=tk.X)
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
            bootstyle="outline-danger"
        )

        self.search_entry.bind("<KeyRelease>", self.filter_tree)

        self.tree_label = ttk.Label(
            self.left_frame, text="Projects", font=("Segoe UI", 11, "bold"))
        self.tree_label.pack(pady=(0, 0))

        self.instruction_label = ttk.Label(
            self.left_frame, text="Double click to select / unselect projects", font=("Segoe UI", 9))
        self.instruction_label.pack(pady=(1, 1))

        tree_frame = ttk.Frame(self.left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))

        # Increase size of projects
        #  rowheight=20
        style.configure("Custom.Treeview", background=Project_Color_Tree,
                        fieldbackground="#f0f0f0", font=("Segoe UI", 9))

        # Projects Left Side
        self.tree = ttk.Treeview(tree_frame, selectmode="extended",style="Custom.Treeview")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        self.tree.bind("<MouseWheel>", self.on_mousewheel)
        self.tree.bind("<Button-4>", self.on_mousewheel)
        self.tree.bind("<Button-5>", self.on_mousewheel)

        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.tag_configure(
            "selected", background=Selected_Project_Background_Color, foreground=Selected_Project_Text_Color)
        
        # Add right-click binding to the tree
        self.tree.bind("<Button-3>", self.on_right_click)

        self.right_frame = ttk.Frame(content_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        self.cart_label = ttk.Label(
            self.right_frame, text="Selected Projects", font=("Segoe UI", 11, "bold"))
        self.cart_label.pack(pady=(0, 0))
        
        self.cart_listbox = Listbox(self.right_frame, height=15, width=20,
                                    selectmode=tk.SINGLE, bg="white", fg="black", font=("Segoe UI", 10))
        self.cart_listbox.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.cart_listbox.bind("<Double-Button-1>", self.on_cart_double_click)

        self.export_button = ttk.Button(self.right_frame, text="Export", image=self.download_icon,
                                        compound=tk.LEFT, command=self.export_selected, bootstyle="success")
        self.export_button.pack(pady=5, padx=20, fill=X)

        self.enter_button = ttk.Button(self.right_frame, text="Select", image=self.plus_icon,
                                       compound=tk.LEFT, command=lambda: self.on_enter_key(None), bootstyle="outline-info")
        self.enter_button.pack(pady=5, padx=20, fill=X)

        self.clear_button = ttk.Button(self.right_frame, text="Clear All", image=self.clear_icon,
                                       compound=tk.LEFT, command=self.clear_selection, bootstyle="info-outline")
        self.clear_button.pack(pady=(0, 5), padx=20, fill=X)

        self.add_today_button = ttk.Button(self.right_frame, text="Recent", image=self.recent_icon,
                                           compound=tk.LEFT, command=self.add_recent_projects, bootstyle="outline-info")
        self.add_today_button.pack(pady=(5, 5), padx=20, fill=X)
        # outline-secondary

        # Settings button
        self.settings_button = ttk.Button(
            self.top_bar,
            text="Settings",
            image=self.settings_icon,
            command=self.open_settings,
            bootstyle="outline-info"
        )
        self.settings_button.pack(side=tk.RIGHT)
        self.settings_tip = Hovertip(self.settings_button, 'Settings')

        self.toggle_icon = self.minus_icon
        self.toggle_button_Close_Folders = ttk.Button(
            self.top_bar,
            image=self.toggle_icon,
            compound=tk.LEFT,
            command=self.toggle_folders,
            bootstyle="outline-info"
        )

        # Create the Music Output Folder button next to toggle button
        self.output_music_folder_button = ttk.Button(
            self.top_bar,
            image=self.music_folder_icon,
            compound=tk.LEFT,
            command=self.open_output_folder,
            bootstyle="outline-info"
        )
        self.output_music_folder_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.music_folder_tip = Hovertip(
            self.output_music_folder_button, 'Open MP3 Output Folder')

        self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))
        self.toggle_tip = Hovertip(
            self.toggle_button_Close_Folders, 'Close folders')

        self.status_label = ttk.Label(
            self.right_frame, text="", font=("Segoe UI", 11), bootstyle="success")
        self.status_label.pack(pady=(0, 10))

        self.populate_tree(Dir_FLP_Projects)
        self.root.bind("<Return>", self.on_enter_key)
    
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
            self.restore_tree_state()
            return

        # Store current tree state if not already stored
        if not self.original_tree_state:
            self.store_tree_state()

        # First, hide all items
        for item in self.tree.get_children():
            self.hide_item_and_children(item)

        # Show only FLP files that match the search term
        for item_id, item_text in self.all_items.items():
            # Only show items that are FLP files (have a path in path_map)
            if item_id in self.path_map and search_term in item_text.lower():
                self.show_item_and_parents(item_id)

        # Additionally, show folders that contain matching FLP files
        for item_id in self.tree.get_children():
            # Check if this folder has any children that are FLP files matching the search
            has_matching_flp = False
            for child in self.tree.get_children(item_id):
                if child in self.path_map and search_term in self.all_items[child].lower():
                    has_matching_flp = True
                    break

            if has_matching_flp:
                self.tree.reattach(item_id, self.tree.parent(item_id), 'end')
                self.tree.item(item_id, open=True)
                # Show all matching FLP files in this folder
                for child in self.tree.get_children(item_id):
                    if child in self.path_map and search_term in self.all_items[child].lower():
                        self.tree.reattach(child, item_id, 'end')

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
        if not self.settings_open:
            global Output_Folder_Path

            # Hide main UI
            self.left_frame.pack_forget()
            self.right_frame.pack_forget()
            self.toggle_button_Close_Folders.pack_forget()

            # Change heading
            self.heading.config(text="Settings")

            # Create the settings frame
            self.settings_frame = ttk.Frame(self.root)
            self.settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Create two sub-frames inside settings_frame
            self.settings_left = ttk.Frame(self.settings_frame)
            self.settings_left.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.settings_right = ttk.Frame(self.settings_frame)
            self.settings_right.pack(
                side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)


            # ✅ Kevin label on the left side
            self.kevin_label = ttk.Label(
                self.settings_left,
                text="kevin",
                font=("Segoe UI", 24, "bold"),
                foreground="#34b1eb"
            )
            self.kevin_label.pack(anchor="center", expand=True)

            # Settings title
            label = ttk.Label(self.settings_right, text="Settings",
                            font=("Segoe UI", 14, "bold"))
            label.pack(pady=10)

            # Output Folder Picker
            output_folder_frame = ttk.Frame(self.settings_right)
            output_folder_frame.pack(fill=tk.X, pady=10)

            self.output_folder_label = ttk.Label(
                output_folder_frame, text="Output Folder:")
            self.output_folder_label.pack(side=tk.LEFT, padx=(0, 5))

            self.output_folder_entry = ttk.Entry(output_folder_frame)
            self.output_folder_entry.pack(
                side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            self.output_folder_entry.insert(0, Output_Folder_Path)

            self.browse_button = ttk.Button(
                output_folder_frame,
                text="Browse",
                command=self.browse_output_folder,
                bootstyle="info"
            )
            self.browse_button.pack(side=tk.LEFT)

            # Show close button and update settings button
            self.close_button.pack(side=tk.RIGHT, padx=(0, 10))
            self.settings_button.config(text="Save Settings", image='')
            self.settings_open = True

        else:
            # Save output path
            new_path = self.output_folder_entry.get().strip()
            if not os.path.isdir(new_path):
                messagebox.showerror(
                    "Error", "The specified directory does not exist.")
                return
            Output_Folder_Path = new_path

            # Destroy settings UI
            self.settings_frame.destroy()
            self.settings_open = False

            # Restore header and UI
            self.heading.config(text=f"🎵 {Application_Name}")
            self.settings_button.config(text="", image=self.settings_icon)
            self.close_button.pack_forget()
            self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
            self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))
            self.output_music_folder_button.pack(side=tk.RIGHT, padx=(0, 10))


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

        # Restore hidden UI elements
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))
        self.output_music_folder_button.pack(side=tk.RIGHT, padx=(0, 10))

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
                    self.tree.item(item_id, tags=("selected",))
        self.refresh_cart()

    def populate_tree(self, parent_path, parent_node=""):
        entries = sorted(os.listdir(parent_path))
        for entry in entries:
            full_path = os.path.join(parent_path, entry)
            if "Backup" in full_path.split(os.sep):
                continue
            if os.path.isdir(full_path):
                contains_flp = any(os.path.isfile(os.path.join(full_path, f)) and f.lower(
                ).endswith(".flp") for f in os.listdir(full_path))
                if contains_flp:
                    node = self.tree.insert(
                        parent_node, "end", text=entry, open=True)
                    self.all_items[node] = entry  # Store for filtering
                    self.populate_tree(full_path, node)
            elif entry.lower().endswith(".flp"):
                clean_name = re.sub(r"\.flp$", "", entry, flags=re.IGNORECASE)
                item_id = self.tree.insert(
                    parent_node, "end", text=clean_name, values=(full_path,))
                self.all_items[item_id] = clean_name  # Store for filtering
                self.path_map[item_id] = full_path

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
                self.tree.item(item_id, tags=("selected",))
        self.refresh_cart()

    def select_range(self, new_item_id):
        if self.last_selected_item is None:
            self.selected_files.add(self.path_map[new_item_id])
            self.tree.item(new_item_id, tags=("selected",))
            self.last_selected_item = new_item_id
            return
        start_idx = self.tree.index(self.last_selected_item)
        end_idx = self.tree.index(new_item_id)
        for idx in range(min(start_idx, end_idx), max(start_idx, end_idx) + 1):
            item_id = self.tree.get_children()[idx]
            if item_id in self.path_map:
                self.selected_files.add(self.path_map[item_id])
                self.tree.item(item_id, tags=("selected",))
        self.last_selected_item = new_item_id

    def toggle_select(self, item_id):
        file_path = self.path_map[item_id]
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self.tree.item(item_id, tags=())
        else:
            self.selected_files.add(file_path)
            self.tree.item(item_id, tags=("selected",))
        self.last_selected_item = item_id

    def on_cart_double_click(self, event):
        selection = self.cart_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        name = self.cart_listbox.get(index)
        file_to_remove = None
        for path in self.selected_files:
            if re.sub(r"\.flp$", "", os.path.basename(path), flags=re.IGNORECASE) == name:
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
            name = re.sub(r"\.flp$", "", os.path.basename(
                path), flags=re.IGNORECASE)
            self.cart_listbox.insert(tk.END, name)

    def export_selected(self):
            # Clear the status completely and force GUI update
        self.status_label.config(text="")
        self.status_label.update()
        self.root.update_idletasks()  # Force complete GUI refresh

        if not self.selected_files:
            self.status_label.config(text="No files selected.", bootstyle="primary")
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
            self.status_label.config(
                text=f"Export failed: {str(e)}",
                bootstyle="danger")
            self.status_label.update()

    def clear_selection(self):
        for item_id in self.path_map:
            self.tree.item(item_id, open=False, tags=())
        self.selected_files.clear()
        self.cart_listbox.delete(0, tk.END)
        self.status_label.config(
            text="Selection cleared.", bootstyle="primary")

    def add_recent_projects(self):
        today = datetime.date.today()
        today_str = today.strftime("%d-%m-%Y")
        file_paths = get_file_paths(Dir_FLP_Projects)

        # First count all today's files (regardless of selection status)
        total_today_files = 0
        for modified_date in file_paths.values():
            if datetime.datetime.fromtimestamp(modified_date).strftime("%d-%m-%Y") == today_str:
                total_today_files += 1

        # Now count how many were actually added (not previously selected)
        added = 0
        for file_path, modified_date in file_paths.items():
            if datetime.datetime.fromtimestamp(modified_date).strftime("%d-%m-%Y") == today_str:
                if file_path not in self.selected_files:
                    self.selected_files.add(file_path)
                    for item_id, path in self.path_map.items():
                        if path == file_path:
                            self.tree.item(item_id, tags=("selected",))
                            break
                    added += 1

        self.refresh_cart()

        if total_today_files == 0:
            self.status_label.config(
                text="No files modified today.", bootstyle="primary")
        else:
            if added > 0:
                # Show how many new files were added
                Recent_Project_Label = "project" if added == 1 else "projects"
                self.status_label.config(
                    text=f"{added}\nrecent {Recent_Project_Label} added.", bootstyle="primary")
            else:
                # Show that all today's files were already selected
                Recent_Project_Label = "project" if total_today_files == 1 else "projects"
                #self.status_label.config(text=f"All {total_today_files} recent {Recent_Project_Label} already selected.", bootstyle="info")
                self.status_label.config(
                    text=f"{total_today_files} recent {Recent_Project_Label} added.", bootstyle="primary")

    def on_mousewheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.tree.yview_scroll(Mouse_Scroll_Speed * delta, "units")
    
    # Right click opens the file, test at home if it opens in FL
    def on_right_click(self, event):
        """Handle right-click to show context menu"""
        item_id = self.tree.identify_row(event.y)
        self.context_item = item_id  # Store the clicked item
        
        if item_id and item_id in self.path_map:
            # Create context menu
            self.context_menu = tk.Menu(self.root, tearoff=0)
            self.context_menu.add_command(
                label="Open File", 
                command=self.open_selected_file
            )
            self.context_menu.add_command(
                label="Open Folder", 
                command=self.open_containing_folder
            )
            
            # Show menu at cursor position
            self.context_menu.post(event.x_root, event.y_root)

    def open_selected_file(self):
        """Open the selected file directly"""
        if hasattr(self, 'context_item') and self.context_item in self.path_map:
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
        if hasattr(self, 'context_item') and self.context_item in self.path_map:
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


# === START APP ===
if __name__ == "__main__":
    style = Style("pulse" if USE_DARK_MODE else "flatly")
    root = style.master
    app = FLPExporterUI(root)
    root.mainloop()
