from PyQt5 import QtWidgets, QtGui, QtCore
import os
import re
import subprocess
import datetime

# === CONFIG ===
USE_DARK_MODE = False
ROOT_FOLDER = r"C:\Users\Kfoen\Documents\Image-Line\FL Studio\Projects\FL 21 - projects"
OUTPUT_FOLDER = r"C:\Users\Kfoen\Documents\Docs KF\FL SONGS MP3\Python_Audio_Output\A"
FL_PATH = r"C:\Program Files\Image-Line\FL Studio 21"
PROCESSOR = "FL64.exe"

# Set Dark Mode Flag
Dark_Mode_Active = USE_DARK_MODE


def get_file_paths(root_directory):
    file_paths = {}
    for dirpath, _, filenames in os.walk(root_directory):
        if "Backup" in dirpath.split(os.sep):
            continue
        for filename in filenames:
            if filename.lower().endswith(".flp"):
                file_path = os.path.join(dirpath, filename)
                modified_date = os.path.getmtime(file_path)
                file_paths[file_path] = modified_date
    return file_paths


def export_flp_to_mp3(file_path):
    cmd = f'cd "{FL_PATH}" & {PROCESSOR} /R /Emp3 "{file_path}" /O"{OUTPUT_FOLDER}"'
    subprocess.call(cmd, shell=True)


class FLPExporterUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎵 FLP to MP3 Exporter")
        self.setGeometry(100, 100, 900, 600)

        # Determine the theme (light or dark)
        self.set_style()

        self.selected_files = set()
        self.path_map = {}

        self.init_ui()
        self.populate_tree(ROOT_FOLDER)

    def set_style(self):
        if Dark_Mode_Active:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2c2f33;
                    color: #ffffff;
                    font-family: Segoe UI;
                }
                QPushButton {
                    background-color: transparent;
                    color: #000000;
                    border: 2px solid #7289da;
                    padding: 8px;
                    border-radius: 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #7289da;
                    color: #ffffff;
                }
                QTreeWidget, QListWidget {
                    background-color: #23272a;
                    border: 1px solid #99aab5;
                    border-radius: 5px;
                }
                QLabel {
                    font-size: 12pt;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    color: #000000;
                    font-family: Segoe UI;
                }
                QPushButton {
                    background-color: transparent;
                    color: #000000;
                    border: 2px solid #4CAF50;
                    padding: 8px;
                    border-radius: 8px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #4CAF50;
                    color: #ffffff;
                }
                QTreeWidget, QListWidget {
                    background-color: #f4f4f4;
                    border: 1px solid #b0b0b0;
                    border-radius: 5px;
                }
                QLabel {
                    font-size: 12pt;
                }
            """)

    def init_ui(self):
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)

        # Left panel (Project Tree)
        left_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(left_layout, 2)

        left_layout.addWidget(QtWidgets.QLabel("Projects"))
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setSelectionMode(
            QtWidgets.QAbstractItemView.MultiSelection)  # Enable multi-select
        self.tree.itemDoubleClicked.connect(self.handle_double_click_tree)
        left_layout.addWidget(self.tree)

        # Right panel (Selected Files + Buttons)
        right_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(right_layout, 1)

        right_layout.addWidget(QtWidgets.QLabel("Selected Projects"))
        self.cart = QtWidgets.QListWidget()
        self.cart.itemDoubleClicked.connect(self.handle_double_click_cart)
        right_layout.addWidget(self.cart)

        self.export_btn = self.create_button("Export", self.export_selected)
        self.select_btn = self.create_button("Select", self.select_highlighted)
        self.clear_btn = self.create_button("Clear All", self.clear_selection)
        self.today_btn = self.create_button("Recent", self.add_today_projects)

        for btn in [self.export_btn, self.select_btn, self.clear_btn, self.today_btn]:
            right_layout.addWidget(btn)

        self.status_label = QtWidgets.QLabel("")
        right_layout.addWidget(self.status_label)

        self.setCentralWidget(container)

    def create_button(self, text, callback):
        btn = QtWidgets.QPushButton(text)
        btn.clicked.connect(callback)

        # Assigning icons after QApplication is created
        if text == "Export":
            btn.setIcon(download_icon)
        elif text == "Select":
            btn.setIcon(plus_icon)
        elif text == "Clear All":
            btn.setIcon(clear_icon)
        elif text == "Recent":
            btn.setIcon(recent_icon)

        btn.setStyleSheet("background-color: transparent; color: black;")
        return btn

    def populate_tree(self, parent_path, parent_node=None):
        try:
            entries = sorted(os.listdir(parent_path))
        except PermissionError:
            return

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
                    node = QtWidgets.QTreeWidgetItem([entry])
                    if parent_node:
                        parent_node.addChild(node)
                    else:
                        self.tree.addTopLevelItem(node)
                    self.populate_tree(full_path, node)
            elif entry.lower().endswith(".flp"):
                clean_name = re.sub(r"\.flp$", "", entry, flags=re.IGNORECASE)
                item = QtWidgets.QTreeWidgetItem([clean_name])
                # ✅ store full path
                item.setData(0, QtCore.Qt.UserRole, full_path)
                if parent_node:
                    parent_node.addChild(item)
                else:
                    self.tree.addTopLevelItem(item)

    def handle_double_click_tree(self, item, _):
        # Retrieve the file path stored in the item's UserRole data
        file_path = item.data(0, QtCore.Qt.UserRole)

        if file_path and os.path.isfile(file_path) and file_path.lower().endswith(".flp"):
            # Toggle selection logic
            if file_path in self.selected_files:
                self.selected_files.remove(file_path)
                item.setBackground(0, QtGui.QBrush(
                    QtGui.QColor("transparent")))  # Reset background
            else:
                self.selected_files.add(file_path)
                # Highlight selected file
                item.setBackground(0, QtGui.QBrush(QtGui.QColor("#7289da")))

            # Update the list of selected files
            self.refresh_cart()

    def handle_double_click_cart(self, item):
        file_name = item.text()
        file_to_remove = None
        for path in self.selected_files:
            if re.sub(r"\.flp$", "", os.path.basename(path), flags=re.IGNORECASE) == file_name:
                file_to_remove = path
                break
        if file_to_remove:
            self.selected_files.remove(file_to_remove)
            for item, path in self.path_map.items():
                if path == file_to_remove:
                    item.setBackground(0, QtGui.QBrush(
                        QtGui.QColor("transparent")))
            self.refresh_cart()

    def refresh_cart(self):
        self.cart.clear()
        for path in sorted(self.selected_files):
            name = re.sub(r"\.flp$", "", os.path.basename(
                path), flags=re.IGNORECASE)
            self.cart.addItem(name)

    def select_highlighted(self):
        selected = self.tree.selectedItems()
        for item in selected:
            if item in self.path_map:
                file_path = self.path_map[item]
                if file_path not in self.selected_files:
                    self.selected_files.add(file_path)
                    item.setBackground(
                        0, QtGui.QBrush(QtGui.QColor("#7289da")))
        self.refresh_cart()

    def export_selected(self):
        if not self.selected_files:
            self.status_label.setText("No files selected.")
            return

        total = len(self.selected_files)
        for idx, path in enumerate(self.selected_files, 1):
            print(f"[{idx}/{total}] Exporting {os.path.basename(path)}")
            export_flp_to_mp3(path)
        self.status_label.setText("Export complete!")

    def clear_selection(self):
        for item in self.tree.selectedItems():
            item.setBackground(0, QtGui.QBrush(QtGui.QColor("transparent")))
        self.selected_files.clear()
        self.cart.clear()
        self.status_label.setText("Selection cleared.")

    def add_today_projects(self):
        today = datetime.date.today().strftime("%d-%m-%Y")
        file_paths = get_file_paths(ROOT_FOLDER)
        for file_path, mod_time in file_paths.items():
            mod_date = datetime.datetime.fromtimestamp(
                mod_time).strftime("%d-%m-%Y")
            if mod_date == today and file_path not in self.selected_files:
                self.selected_files.add(file_path)
                for item, path in self.path_map.items():
                    if path == file_path:
                        item.setBackground(
                            0, QtGui.QBrush(QtGui.QColor("#7289da")))
        self.refresh_cart()


def load_icon(icon_path):
    return QtGui.QIcon(icon_path)


if __name__ == "__main__":
    # Initialize the QApplication instance first
    app = QtWidgets.QApplication([])

    # Load icons
    download_icon = load_icon("Media/Icons/download.png")
    plus_icon = load_icon("Media/Icons/plus.png")
    clear_icon = load_icon("Media/Icons/clear.png")
    recent_icon = load_icon("Media/Icons/recent.png")

    window = FLPExporterUI()
    window.show()
    app.exec_()
