# Old Gui
import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk


# === CONFIG ===
USE_DARK_MODE = False  # Toggle between dark mode and light mode
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 20 - projects"
#Root_Folder_K2 = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 12 - projects"

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
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # === THEME ===
        if USE_DARK_MODE:
            self.bg_color = "#2C2F34"
            self.fg_color = "white"
            self.listbox_bg = "#3D3F46"
            self.listbox_fg = "white"
            self.button_bg = "#4A4A4A"
            self.button_fg = "white"
            self.selected_tag_bg = "#FEB335"
            self.selected_tag_fg = "black"
        else:
            self.bg_color = "SystemButtonFace"
            self.fg_color = "black"
            self.listbox_bg = "white"
            self.listbox_fg = "black"
            self.button_bg = None
            self.button_fg = None
            self.selected_tag_bg = "#FEB335"
            self.selected_tag_fg = "black"

        root.configure(bg=self.bg_color)

        style = ttk.Style()
        style.theme_use('classic')
        style.configure("Treeview",
                        rowheight=22,
                        background=self.bg_color if USE_DARK_MODE else "white",
                        foreground=self.fg_color if USE_DARK_MODE else "black",
                        fieldbackground=self.bg_color if USE_DARK_MODE else "white")
        style.map("Treeview",
                  background=[
                      ('selected', '#3D3F46' if USE_DARK_MODE else '#D9D9D9')],
                  foreground=[
                      ('selected', 'white' if USE_DARK_MODE else 'black')]
                  )

        self.selected_files = set()
        self.path_map = {}

        self.paned = tk.PanedWindow(
            root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg=self.bg_color)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # === LEFT SIDE ===
        self.left_frame = tk.Frame(self.paned, bg=self.bg_color)
        self.paned.add(self.left_frame, minsize=400)

        self.tree_label = tk.Label(self.left_frame, text="Projects", font=("Arial", 10, "bold"),
                                   bg=self.bg_color, fg=self.fg_color)
        self.tree_label.pack(pady=(10, 0))

        self.instruction_label = tk.Label(
            self.left_frame, text="Double click to select / unselect projects", font=("Arial", 10),
            anchor="w", bg=self.bg_color, fg=self.fg_color
        )
        self.instruction_label.pack(pady=(1, 1), padx=1)

        tree_frame = tk.Frame(self.left_frame, bg=self.bg_color)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(5, 10))

        self.tree = ttk.Treeview(tree_frame, selectmode="extended")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<MouseWheel>", self.on_mousewheel)  # Windows
        self.tree.bind("<Button-4>", self.on_mousewheel)   # Linux scroll up
        self.tree.bind("<Button-5>", self.on_mousewheel)   # Linux scroll down

        scrollbar = tk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)

        self.tree.bind("<Double-1>", self.on_tree_double_click)
        self.tree.tag_configure(
            "selected", background=self.selected_tag_bg, foreground=self.selected_tag_fg)

        # === RIGHT SIDE ===
        self.right_frame = tk.Frame(self.paned, bg=self.bg_color)
        self.paned.add(self.right_frame, minsize=300)

        self.cart_label = tk.Label(
            self.right_frame, text="Selected Projects", font=("Arial", 10, "bold"),
            bg=self.bg_color, fg=self.fg_color
        )
        self.cart_label.pack(pady=(10, 0))

        self.tree.tag_configure("selected_projects", background="red")

        self.cart_listbox = tk.Listbox(
            self.right_frame, height=20, selectmode=tk.SINGLE,
            bg=self.listbox_bg, fg=self.listbox_fg
        )
        self.cart_listbox.pack(fill=tk.BOTH, expand=True,
                               padx=10, pady=(5, 10))

        self.export_button = tk.Button(
            self.right_frame, text="Export Selected to MP3", command=self.export_selected,
            bg=self.button_bg, fg=self.button_fg
        )
        self.export_button.pack(pady=5)

        self.clear_button = tk.Button(
            self.right_frame, text="Clear All", command=self.clear_selection,
            bg=self.button_bg, fg=self.button_fg
        )
        self.clear_button.pack(pady=(0, 10))

        self.status_label = tk.Label(
            self.right_frame, text="", font=("Segoe UI", 9), fg="green", bg=self.bg_color
        )
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

    # Future feature, change value 3, to accomodate for lots of files in folder
    def on_mousewheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.tree.yview_scroll(3 * delta, "units")


# === START APP ===
if __name__ == "__main__":
    root = tk.Tk()
    app = FLPExporterUI(root)
    root.mainloop()
