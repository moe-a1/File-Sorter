import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog


class FileSorter:
    def __init__(self, window):
        self.window = window
        self.window.title("File-Sorter")
        self.window.geometry("400x200")

        self.custom_preferences = {}
        self.use_desktop_as_source = tk.BooleanVar()

        self.create_tkinter_objs(40, 2)

    def create_tkinter_objs(self, button_width, button_height):
        self.label = tk.Label(self.window, text="Choose an organization method:")
        self.label.pack()

        self.extension_button = tk.Button(self.window, text="Organize by file extension", command=self.organize_by_extension, width=button_width, height=button_height)
        self.extension_button.pack(expand=True)
        self.custom_button = tk.Button(self.window, text="Custom organization based on name patterns", command=self.organize_by_custom_preference, width=button_width, height=button_height)
        self.custom_button.pack(expand=True)
        self.source_checkbox = tk.Checkbutton(self.window, text="Use desktop as source directory", variable=self.use_desktop_as_source)
        self.source_checkbox.pack()

    def get_path(self):
        if self.use_desktop_as_source.get():
            return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return filedialog.askdirectory(title="Source Folder")

    def organize_by_extension(self):
        path = self.get_path()
        extensions_dir = {}
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path) and not file.endswith('.lnk'):
                file_extension = os.path.splitext(file)[-1].lower()
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
            for file_pattern, destination_folder in self.custom_preferences.items():
                for file in os.listdir(path):
                    if os.path.isfile(os.path.join(path, file)) and file_pattern.lower() in file.lower() and not file.endswith('.lnk'):
                        new_location = os.path.join(destination_folder, file)
                        shutil.move(os.path.join(path, file), new_location)
                        print(f"Moved {file} to {destination_folder}")
            messagebox.showinfo("Success", "Custom preference organization complete.")


def main():
    tkinter = tk.Tk()
    FileSorter(tkinter)
    tkinter.mainloop()


main()
