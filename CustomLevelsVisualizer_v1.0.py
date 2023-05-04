import os
import csv
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog

# Locate the CustomLevels folder
custom_levels_dir = "C:/Program Files (x86)/Steam/steamapps/common/Beat Saber/Beat Saber_Data/CustomLevels"
if not os.path.exists(custom_levels_dir):
    # Prompt the user to manually select the folder
    root = tk.Tk()
    root.withdraw()
    custom_levels_dir = tk.filedialog.askdirectory(title="Select the 'CustomLevels' folder")

class CustomLevel:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.info_path = os.path.join(dir_path, "info.dat")
        self.cover_path = os.path.join(dir_path, "cover.png")
        if not os.path.exists(self.cover_path):
            self.cover_path = os.path.join(dir_path, "cover.jpg")
        self.song_name = ""
        self.song_author = ""
        self.level_author = ""
        with open(self.info_path, "r") as f:
            data = f.read().splitlines()
        for line in data:
            if "_songName" in line:
                self.song_name = line.split(":")[1][1:-1]
            elif "_songAuthorName" in line:
                self.song_author = line.split(":")[1][1:-1]
            elif "_levelAuthorName" in line:
                self.level_author = line.split(":")[1][1:-1]

class App:
    def __init__(self, root):
        self.root = root
        self.levels = []
        self.selected_level = None
        self.selected_img = None
        self.create_widgets()
        self.load_levels()

    def create_widgets(self):
        # Create the left panel that lists all the custom levels
        self.left_panel = tk.Frame(self.root)
        self.left_panel.pack(side="left", fill="y")
        self.levels_listbox = tk.Listbox(self.left_panel)
        self.levels_listbox.pack(side="left", fill="y")
        self.levels_listbox.bind("<<ListboxSelect>>", self.on_select_level)

        # Create the right panel that displays the selected level's image and info
        self.right_panel = tk.Frame(self.root)
        self.right_panel.pack(side="right", fill="both", expand=True)
        self.img_label = tk.Label(self.right_panel)
        self.img_label.pack(side="top", fill="both", expand=True)
        self.info_label = tk.Label(self.right_panel, wraplength=300)
        self.info_label.pack(side="bottom", fill="x")

        # Create the export and import buttons
        self.export_button = tk.Button(self.left_panel, text="Export", command=self.export_levels)
        self.export_button.pack(side="bottom")
        self.import_button = tk.Button(self.left_panel, text="Import", command=self.import_levels)
        self.import_button.pack(side="bottom")

    def load_levels(self):
        # Load all the custom levels in the CustomLevels folder
        for dir_path, dir_names, file_names in os.walk(custom_levels_dir):
            for dir_name in dir_names:
                level_dir = os.path.join(dir_path, dir_name)
                self.levels.append(CustomLevel(level_dir))
                self.levels_listbox.insert("end", dir_name)

    def on_select_level(self, event):
        # Display the selected level's image and info on the right panel
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_level = self.levels[index]
            img = Image.open(self.selected_level.cover_path)
            img = img.resize((300, 300), Image.ANTIALIAS)
            self.selected_img = ImageTk.PhotoImage(img)
            self.img_label.configure(image=self.selected_img)
            self.info_label.configure(text="Song Name: {}\nSong Author: {}\nLevel Author: {}".format(self.selected_level.song_name, self.selected_level.song_author, self.selected_level.level_author))

    def export_levels(self):
        # Export the listed levels to a CSV file
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Export Levels")
        if file_path:
            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                for level in self.levels:
                    writer.writerow([level.dir_path, level.song_name, level.song_author, level.level_author])

    def import_levels(self):
        # Import a CSV file of levels
        file_path = tk.filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Import Levels")
        if file_path:
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.levels.append(CustomLevel(row[0]))
                    self.levels_listbox.insert("end", os.path.basename(row[0]))

root = tk.Tk()
root.title("Custom Levels Visualizer")
app = App(root)
root.mainloop()