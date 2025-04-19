import os
import re
import subprocess
import ttkbootstrap
import ttkbootstrap as ttk  # NEW: Use ttkbootstrap instead of tkinter
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import Listbox  # Listbox still from tkinter
import tkinter as tk  # ✅ Fixes all 'tk' constants

# === CONFIG ===
USE_DARK_MODE = False  # Toggle between dark mode and light mode
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
Output_Folder_Path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"


def export_flp_to_mp3(file_path):
    Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /Emp3 "{file_path}" /O"{Output_Folder_Path}"'
    subprocess.call(Export_FLP_to_MP3, shell=True)


class FLPExporterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FLP Exporter")
        self.root.geometry("500x600+30+20")
        self.root.resizable(False, False)

        # === Heading ===
        self.heading = ttk.Label(self.root, text="🎵 FLP to MP3 Exporter", font=(
            "Segoe UI", 16, "bold"), bootstyle="info")
        self.heading.pack(pady=(0, 5))

        self.selected_files = set()
        self.path_map = {}
        self.last_selected_item = None

        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # === LEFT SIDE ===
        self.left_frame = ttk.Frame(content_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree_label = ttk.Label(
            self.left_frame, text="Projects", font=("Segoe UI", 11, "bold"))
        self.tree_label.pack(pady=(0, 0))

        self.instruction_label = ttk.Label(
            self.left_frame, text="Double click to select / unselect projects", font=("Segoe UI", 9)
        )
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
            "selected", background="#FEB335", foreground="black")

        # === RIGHT SIDE ===
        self.right_frame = ttk.Frame(content_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.cart_label = ttk.Label(
            self.right_frame, text="Selected Projects", font=("Segoe UI", 11, "bold"))
        self.cart_label.pack(pady=(0, 0))

        self.cart_listbox = Listbox(
            self.right_frame, height=20, selectmode=tk.SINGLE,
            bg="white", fg="black", font=("Segoe UI", 10)
        )
        self.cart_listbox.pack(fill=tk.BOTH, expand=True,
                               padx=10, pady=(5, 10))
        # NEW: Remove on double-click
        self.cart_listbox.bind("<Double-Button-1>", self.on_cart_double_click)

        self.export_button = ttk.Button(
            self.right_frame, text="Export Selected to MP3", command=self.export_selected, bootstyle="success"
        )
        self.export_button.pack(pady=5, padx=20, fill=X)

        self.enter_button = ttk.Button(
            self.right_frame, text="Select Project", command=lambda: self.on_enter_key(None), bootstyle="primary"
        )
        self.enter_button.pack(pady=5, padx=20, fill=X)

        self.clear_button = ttk.Button(
            self.right_frame, text="Clear All", command=self.clear_selection, bootstyle="secondary"
        )
        self.clear_button.pack(pady=(0, 5), padx=20, fill=X)

        self.status_label = ttk.Label(
            self.right_frame, text="", font=("Segoe UI", 9), bootstyle="success")
        self.status_label.pack(pady=(0, 10))

        self.populate_tree(Root_Folder_K2)
        self.root.bind("<Return>", self.on_enter_key)

    def on_enter_key(self, event):
        item_id = self.tree.focus()
        if not item_id or item_id not in self.path_map:
            return

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
                contains_flp = any(
                    os.path.isfile(os.path.join(full_path, f)
                                   ) and f.lower().endswith(".flp")
                    for f in os.listdir(full_path)
                )
                if contains_flp:
                    node = self.tree.insert(
                        parent_node, "end", text=entry, open=False)
                    self.populate_tree(full_path, node)
            elif entry.lower().endswith(".flp"):
                clean_name = re.sub(r"\.flp$", "", entry, flags=re.IGNORECASE)
                item_id = self.tree.insert(
                    parent_node, "end", text=clean_name, values=(full_path,))
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
            self.selected_files.add(file_path)
            self.tree.item(item_id, tags=("selected",))

        self.refresh_cart()

    def on_cart_double_click(self, event):  # NEW: Remove from selection
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

        total = len(self.selected_files)
        for idx, path in enumerate(self.selected_files, 1):
            print(f"[{idx}/{total}] Exporting {os.path.basename(path)}")
            export_flp_to_mp3(path)

        self.status_label.config(
            text=f"{total} project(s) exported.",
            bootstyle="success"
        )

    def clear_selection(self):
        for item_id in self.path_map:
            self.tree.item(item_id, tags=())
        self.selected_files.clear()
        self.cart_listbox.delete(0, tk.END)
        self.status_label.config(
            text="Selection cleared.", bootstyle="secondary")

    def on_mousewheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.tree.yview_scroll(3 * delta, "units")


# === START APP ===
if __name__ == "__main__":
    style = Style("darkly" if USE_DARK_MODE else "flatly")
    root = style.master
    app = FLPExporterUI(root)
    root.mainloop()
