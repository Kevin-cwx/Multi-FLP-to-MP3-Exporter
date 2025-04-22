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


# === CONFIG ===
USE_DARK_MODE = False
Dir_FLP_Projects = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
Output_Folder_Path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"


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


def export_flp_to_mp3(file_path):
    Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /Emp3 "{file_path}" /O"{Output_Folder_Path}"'
    subprocess.call(Export_FLP_to_MP3, shell=True)


class FLPExporterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FLP to MP3 Exporter")
        self.root.geometry("600x600+30+20")
        self.root.resizable(False, False)
        self.root.title("FLP to MP3 Exporter")
        transparent_icon = tk.PhotoImage(width=1, height=1)
        self.root.iconbitmap(r"Media/icons/FL21 - Icon.ico")
        Background_Color = "white"
        self.root.configure(bg=Background_Color)
        self.folders_expanded = True
        self.settings_open = False

        # Create top bar frame first
        self.top_bar = ttk.Frame(self.root)
        self.top_bar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Add heading to the top bar frame (left side)
        self.heading = ttk.Label(self.top_bar, text="🎵 FLP to MP3 Exporter",
                                 font=("Segoe UI", 16, "bold"), bootstyle="info", foreground="black")
        self.heading.pack(side=tk.LEFT, pady=0)

        style = ttk.Style()

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
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X,
                               expand=True, padx=(0, 5))
        
        self.search_entry.bind("<KeyRelease>", self.filter_tree)

        self.tree_label = ttk.Label(
            self.left_frame, text="Projects", font=("Segoe UI", 11, "bold"))
        self.tree_label.pack(pady=(0, 0))

        self.instruction_label = ttk.Label(
            self.left_frame, text="Double click to select / unselect projects", font=("Segoe UI", 9))
        self.instruction_label.pack(pady=(1, 1))

        tree_frame = ttk.Frame(self.left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 10))

        self.tree = ttk.Treeview(tree_frame, selectmode="extended")
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
            "selected", background="#34b1eb", foreground="black")

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
                                           compound=tk.LEFT, command=self.add_today_projects, bootstyle="outline-info")
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
        self.music_folder_button = ttk.Button(
            self.top_bar,
            image=self.music_folder_icon,
            compound=tk.LEFT,
            command=self.open_output_folder,
            bootstyle="outline-info"
        )
        self.music_folder_button.pack(side=tk.RIGHT, padx=(0, 10))
        self.music_folder_tip = Hovertip(
            self.music_folder_button, 'Open MP3 Output Folder')

        self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))
        self.toggle_tip = Hovertip(
            self.toggle_button_Close_Folders, 'Close folders')

        self.status_label = ttk.Label(
            self.right_frame, text="", font=("Segoe UI", 9), bootstyle="success")
        self.status_label.pack(pady=(0, 10))

        self.populate_tree(Dir_FLP_Projects)
        self.root.bind("<Return>", self.on_enter_key)

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

        # Show items that match the search term
        for item_id, item_text in self.all_items.items():
            if search_term in item_text.lower():
                self.show_item_and_parents(item_id)
                # If it's a folder, look for matches in children
                if self.tree.get_children(item_id):
                    for child in self.tree.get_children(item_id):
                        child_text = self.tree.item(child)['text']
                        if search_term in child_text.lower():
                            self.tree.reattach(child, item_id, 'end')
                            self.tree.item(item_id, open=True)
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
                self.tree.item(item, open=False)
                self.hide_item_and_children(item)

        # Show items that match the search term
            for item_id, item_text in self.all_items.items():
                if search_term in item_text.lower():
                    self.show_item_and_parents(item_id)
                    # If it's a folder, look for matches in children
                    if self.tree.get_children(item_id):
                        for child in self.tree.get_children(item_id):
                            child_text = self.tree.item(child)['text']
                            if search_term in child_text.lower():
                                self.tree.reattach(child, item_id, 'end')
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
        if not self.settings_open:
            # Hide the left and right frames and collapse button
            self.left_frame.pack_forget()
            self.right_frame.pack_forget()
            self.toggle_button_Close_Folders.pack_forget()

            # Create and show settings UI
            self.settings_frame = ttk.Frame(self.root)
            self.settings_frame.pack(
                fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Example settings content
            label = ttk.Label(self.settings_frame, text="Settings",
                              font=("Segoe UI", 14, "bold"))
            label.pack(pady=10)

            self.example_entry = ttk.Entry(self.settings_frame)
            self.example_entry.insert(0, "Example setting value")
            self.example_entry.pack(pady=10)

            self.settings_open = True
            self.settings_button.config(text="Save")
        else:
            # Save logic (optional: store settings)
            setting_value = self.example_entry.get()

            # Hide settings UI and restore main UI
            self.settings_frame.pack_forget()
            self.settings_frame.destroy()

            # Show the left and right frames and collapse button again
            self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
            self.toggle_button_Close_Folders.pack(side=tk.RIGHT, padx=(0, 10))

            self.settings_open = False
            self.settings_button.config(text="Settings")

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
        if not self.selected_files:
            self.status_label.config(
                text="No files selected.", bootstyle="danger")
            return
        #self.status_label.config(text="Exporting...", bootstyle="warning")
        self.status_label.update_idletasks()
        total = len(self.selected_files)
        try:
            self.status_label.config(text="", bootstyle="secondary")
            self.status_label.config(text="Exporting...", bootstyle="warning")
            self.status_label.update_idletasks()
            for idx, path in enumerate(self.selected_files, 1):
                print(f"[{idx}/{total}] Exporting {os.path.basename(path)}")
                export_flp_to_mp3(path)
            Exported_project_label = "project" if total == 1 else "projects"
            self.status_label.config(
                text=f"{total} {Exported_project_label} exported.", bootstyle="dark")
        except Exception as e:
            self.status_label.config(
                text=f"Export failed: {str(e)}", bootstyle="danger")

    def clear_selection(self):
        for item_id in self.path_map:
            self.tree.item(item_id, open=False, tags=())
        self.selected_files.clear()
        self.cart_listbox.delete(0, tk.END)
        self.status_label.config(
            text="Selection cleared.", bootstyle="primary")

    def add_today_projects(self):
        today = datetime.date.today()
        today_str = today.strftime("%d-%m-%Y")
        file_paths = get_file_paths(Dir_FLP_Projects)
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
        if added == 0:
            self.status_label.config(
                text="No files modified today.", bootstyle="warning")
        else:
            Recent_Project_Label = "project" if added == 1 else "projects"
            self.status_label.config(
                text=f"{added} recent {Recent_Project_Label} added.", bootstyle="primary")

    def on_mousewheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.tree.yview_scroll(5 * delta, "units")


# === START APP ===
if __name__ == "__main__":
    style = Style("pulse" if USE_DARK_MODE else "flatly")
    root = style.master
    app = FLPExporterUI(root)
    root.mainloop()
