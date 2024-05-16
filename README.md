# File-Sorter

Welcome to File-Sorter, a simple tool to help you organize your files on your computer. This application is built with Python and uses the Tkinter library for a user-friendly graphical interface. File-Sorter allows you to automatically organize files either by their extension or by custom patterns that you define.

## Features

- **Organize by File Extension**: Automatically move files into folders based on their file extensions.
- **Custom Organization**: Set up custom rules to move files based on name patterns into specified directories.
- **Exclude Files**: Specify file names and extensions that you do not want to move.
- **Option to Ignore Shortcuts**: Choose whether to move or ignore shortcut files (`.lnk`) during the extension-based organization.
- **Persistence**: Your settings (excluded files, ignored extensions, etc.) are saved and will be automatically loaded the next time you run the application.

## Requirements

Before you run File-Sorter, you need to ensure that you have Python installed on your system. The application is developed using Python 3.11+, and it is recommended to use the same or newer versions.

## How to Use

1. **Download the Repository**: Clone or download this repository to your local machine.
2. **Run the Application**: Open main.py or open a terminal in the project directory and run the command: (make sure that you run cmd from same directory main.py exists)
```cmd
python main.py
```
3. **Choose Source Folder**: By default, the application uses the Desktop as the source directory, but you can change it by unchecking the "Use desktop as source directory" checkbox and selecting a new directory when you choose an organizing process.
4. **Start Organizing**: Click the appropriate button to start the organization process based on your settings.

## Important Note on First Run

Just a heads up—when you use FileSorter for the first time, it’ll create a file named `options.txt` in the same directory where `main.py` is. This file keeps track of your settings from the last time you used the app, so the next time you open it, everything will be just like you left it. This makes it easier and more convenient for you to keep using the app without having to redo your settings every time.

Enjoy organizing your files with ease using File-Sorter!