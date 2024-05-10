import os
import shutil


def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")


def get_path():
    while True:
        path = input("Enter the source directory path: ").strip()
        if os.path.exists(path) and os.path.isdir(path):
            return path
        else:
            print("Invalid directory. Please enter a valid path.")


def organize_by_extension(path):
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
    return extensions_dir


def get_custom_preferences():
    preferences = {}
    while True:
        file_pattern = input("Enter file name pattern to move (or press Enter to exit): ").strip()
        if not file_pattern:
            break
        destination_folder = input("Enter the full path of the destination folder: ").strip()
        if not os.path.isabs(destination_folder):
            print("Invalid path. Please re-enter file name pattern and a valid absolute path.")
            continue
        preferences[file_pattern] = destination_folder

        add_more = input("Do you want to move more files from current directory? (yes/no): ").strip().lower()
        if add_more not in ['yes', 'y']:
            break
    return preferences


def organize_by_custom_preference(path, preferences):
    for file_pattern, destination_folder in preferences.items():
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and file_pattern.lower() in file.lower():
                new_location = os.path.join(destination_folder, file)
                shutil.move(os.path.join(path, file), new_location)
                print(f"Moved {file} to {destination_folder}")


def get_user_choice():
    while True:
        print("Please choose an organization method:")
        print("1: Organize by file extension")
        print("2: Custom file organization based on name patterns")

        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            desktop_choice = input("Is the task to be performed on the desktop? (yes/no): ").strip().lower()
            if desktop_choice in ['yes', 'y']:
                return choice, get_desktop_path()
            elif desktop_choice in ['no', 'n']:
                return choice, get_path()
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        else:
            print("Invalid choice. Please choose 1 or 2.")


def main():
    continue_organizing = 'yes'
    while continue_organizing.lower() in ['yes', 'y']:
        choice, path = get_user_choice()

        if choice == '1':
            extensions_dir = organize_by_extension(path)
            print("Extension-based organization complete.")
            print(extensions_dir)
        elif choice == '2':
            preferences = get_custom_preferences()
            if preferences:
                organize_by_custom_preference(path, preferences)
                print("Custom preference organization complete.")

        continue_organizing = input("Do you want to do more organizing? (yes/no): ")

    print("Closing File-Sorter.")


main()
