import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


class FileSorter:
    def __init__(self, window):
        self.window = window
        self.window.title("File-Sorter")
        self.window.geometry("400x300")

        self.custom_preferences = {}
        self.ignore_shortcuts = tk.BooleanVar(value=True)
        self.use_desktop_as_source = tk.BooleanVar()
        self.create_tkinter_objs(40, 2)

        self.load_options()
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def create_tkinter_objs(self, button_width, button_height):
        self.label = tk.Label(self.window, text="Choose an organization method:")
        self.label.pack()

        self.extension_button = tk.Button(self.window, text="Organize by file extension", command=self.organize_by_extension, width=button_width, height=button_height)
        self.extension_button.pack(expand=True)
        self.custom_button = tk.Button(self.window, text="Custom organization based on name patterns", command=self.organize_by_custom_preference, width=button_width, height=button_height)
        self.custom_button.pack(expand=True)
        self.source_checkbox = tk.Checkbutton(self.window, text="Use desktop as source directory", variable=self.use_desktop_as_source)
        self.source_checkbox.pack()

        self.ignore_ext_label = tk.Label(self.window, text="Enter extensions to ignore (comma-separated):")
        self.ignore_ext_label.pack()
        self.ignore_ext_entry = tk.Entry(self.window)
        self.ignore_ext_entry.pack()

        self.ignore_shortcuts_checkbox = tk.Checkbutton(self.window, text="Do not move shortcuts (Extension-based organization ONLY)", variable=self.ignore_shortcuts)
        self.ignore_shortcuts_checkbox.pack()

        self.exclude_files_label = tk.Label(self.window, text="Enter file names to exclude (comma-separated):")
        self.exclude_files_label.pack()
        self.exclude_files_entry = tk.Entry(self.window, width=50)
        self.exclude_files_entry.pack(pady=10)

    def update_ignore_extensions(self):
        self.ignore_extensions.clear()
        if self.ignore_shortcuts.get():
            self.ignore_extensions.append('lnk')

        entry_extensions = self.ignore_ext_entry.get().split(',')
        for ext in entry_extensions:
            self.ignore_extensions.append(ext.strip())

    def update_exclude_file_names(self):
        self.exclude_files.clear()
        entry_files = self.exclude_files_entry.get().split(',')
        for file_name in entry_files:
            self.exclude_files.append(file_name.strip())

    def get_path(self):
        if self.use_desktop_as_source.get():
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return filedialog.askdirectory(title="Source Folder")

    def organize_by_extension(self):
        path = self.get_path()
        extensions_dir = {}
        self.update_ignore_extensions()
        self.update_exclude_file_names()
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            file_extension = os.path.splitext(file)[-1].lower()
            file_name = os.path.splitext(file)[0]
            if os.path.isfile(file_path) and file_extension[1:] not in self.ignore_extensions and file_name not in self.exclude_files:
                if file_extension and file_extension not in extensions_dir:
                    ext_dir = os.path.join(path, file_extension[1:])
                    extensions_dir[file_extension] = ext_dir
                    if not os.path.exists(ext_dir):
                        os.makedirs(ext_dir)

                new_location = os.path.join(extensions_dir[file_extension], file)
                shutil.move(file_path, new_location)
                print(f"Moved {file} to {extensions_dir[file_extension]}")
        messagebox.showinfo("Success", "Extension-based organization complete.")

    def get_custom_preferences(self):
        while True:
            file_pattern = simpledialog.askstring("File Pattern", "Enter file name pattern to move (or press Cancel to exit):")
            if file_pattern is None:
                break
            elif file_pattern.strip() == "":
                messagebox.showwarning("Warning", "Please enter a file pattern or click Cancel.")
            else:
                destination_folder = filedialog.askdirectory(title="Destination Folder")
                if destination_folder:
                    self.custom_preferences[file_pattern] = destination_folder
                    if not messagebox.askyesno("Add More", "Do you want to add more preferences from current source folder?"):
                        break

    def organize_by_custom_preference(self):
        path = self.get_path()
        self.custom_preferences = {}
        self.get_custom_preferences()
        if self.custom_preferences:
            self.update_exclude_file_names()
            for file_pattern, destination_folder in self.custom_preferences.items():
                for file in os.listdir(path):
                    if os.path.isfile(os.path.join(path, file)):
                        file_name = os.path.splitext(file)[0]
                        if file_name not in self.exclude_files and file_pattern.lower() in file.lower() and not file.endswith('.lnk'):
                            new_location = os.path.join(destination_folder, file)
                            shutil.move(os.path.join(path, file), new_location)
                            print(f"Moved {file} to {destination_folder}")
            messagebox.showinfo("Success", "Custom preference organization complete.")

    def save_options(self):
        if 'lnk' in self.ignore_extensions:
            self.ignore_extensions.remove('lnk')
        with open("options.txt", "w") as file:
            file.write(",".join(self.ignore_extensions) + "\n")
            file.write(",".join(self.exclude_files) + "\n")
            file.write(str(self.ignore_shortcuts.get()) + "\n")
            file.write(str(self.use_desktop_as_source.get()) + "\n")

    def load_options(self):
        try:
            with open("options.txt", "r") as file:
                options = file.readlines()
                self.ignore_extensions = options[0].strip().split(",")
                self.exclude_files = options[1].strip().split(",")
                self.ignore_shortcuts.set(options[2].strip().lower() == 'true')
                self.use_desktop_as_source.set(options[3].strip().lower() == 'true')

                self.ignore_ext_entry.insert(0, ",".join(self.ignore_extensions))
                self.exclude_files_entry.insert(0, ",".join(self.exclude_files))
        except FileNotFoundError:
            self.ignore_extensions = []
            self.exclude_files = []

    def close(self):
        self.save_options()
        self.window.destroy()


def main():
    tkinter = tk.Tk()
    FileSorter(tkinter)
    tkinter.mainloop()


main()
