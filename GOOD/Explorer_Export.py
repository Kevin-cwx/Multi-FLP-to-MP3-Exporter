import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk

# === CONFIG ===
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
Output_Folder_Path = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"
FL_Studio_Path = r"C:\Program Files\Image-Line\FL Studio 21"
Processor_Type = "FL64.exe"

# === EXPORT FUNCTION ===


def export_flp_to_mp3(file_path):
    Export_FLP_to_MP3 = f'cd "{FL_Studio_Path}" & {Processor_Type} /R /Emp3 "{file_path}" /O"{Output_Folder_Path}"'
    subprocess.call(Export_FLP_to_MP3, shell=True)

# === UI CLASS ===


class FLPExporterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FLP Exporter")
        self.root.geometry("600x500")

        style = ttk.Style()
        style.theme_use('classic')
        style.configure("Treeview", rowheight=22)
        style.map("Treeview")

        self.selected_files = set()
        self.path_map = {}

        # Split layout: left tree, right selected
        self.paned = tk.PanedWindow(
            root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # === LEFT SIDE (Tree) ===
        self.left_frame = tk.Frame(self.paned)
        self.paned.add(self.left_frame, minsize=400)

        # Projects label at the top
        self.tree_label = tk.Label(
            self.left_frame, text="Projects", font=("Arial", 10, "bold"))
        self.tree_label.pack(pady=(10, 0))

        # Instruction label immediately below "Projects"
        self.instruction_label = tk.Label(
            self.left_frame, text="Double click to select / unselect project", font=("Arial", 10), anchor="w")
        # Adjusted padding for closeness
        self.instruction_label.pack(pady=(1, 1), padx=1)

        # Treeview for projects
        self.tree = ttk.Treeview(self.left_frame, selectmode="extended")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.tag_configure("selected", background="#FEB335")

        # === RIGHT SIDE (Cart) ===
        self.right_frame = tk.Frame(self.paned)
        self.paned.add(self.right_frame, minsize=300)

        self.cart_label = tk.Label(
            self.right_frame, text="Selected Projects", font=("Arial", 10, "bold"))
        self.cart_label.pack(pady=(10, 0))

        self.tree.tag_configure("selected_projects", background="lightblue")


        self.cart_listbox = tk.Listbox(
            self.right_frame, height=20, selectmode=tk.SINGLE)
        self.cart_listbox.pack(fill=tk.BOTH, expand=True,
                               padx=10, pady=(5, 10))

        self.export_button = tk.Button(
            self.right_frame, text="Export Selected to MP3", command=self.export_selected)
        self.export_button.pack(pady=5)

        self.clear_button = tk.Button(
            self.right_frame, text="Clear All", command=self.clear_selection)
        self.clear_button.pack(pady=(0, 10))

        self.status_label = tk.Label(
            self.right_frame, text="", font=("Segoe UI", 9), fg="green")
        self.status_label.pack(pady=(0, 10))

        self.populate_tree(Root_Folder_K2)

    def populate_tree(self, parent_path, parent_node=""):
        entries = sorted(os.listdir(parent_path))
        for entry in entries:
            full_path = os.path.join(parent_path, entry)
            if "Backup" in full_path.split(os.sep):
                continue

            if os.path.isdir(full_path):
                contains_flp = any(
                    os.path.isfile(os.path.join(full_path, f))
                    and f.lower().endswith(".flp")
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

    def refresh_cart(self):
        self.cart_listbox.delete(0, tk.END)
        for path in sorted(self.selected_files):
            name = re.sub(r"\.flp$", "", os.path.basename(
                path), flags=re.IGNORECASE)
            self.cart_listbox.insert(tk.END, name)

    def export_selected(self):
        if not self.selected_files:
            self.status_label.config(text="No files selected.", fg="red")
            return

        total = len(self.selected_files)
        for idx, path in enumerate(self.selected_files, 1):
            print(f"[{idx}/{total}] Exporting {os.path.basename(path)}")
            export_flp_to_mp3(path)

        self.status_label.config(
            text=f"{total} project(s) exported to: {Output_Folder_Path}",
            fg="green"
        )

    def clear_selection(self):
        for item_id in self.path_map:
            self.tree.item(item_id, tags=())
        self.selected_files.clear()
        self.cart_listbox.delete(0, tk.END)
        self.status_label.config(text="Selection cleared.", fg="gray")


# === START APP ===
if __name__ == "__main__":
    root = tk.Tk()
    app = FLPExporterUI(root)
    root.mainloop()
