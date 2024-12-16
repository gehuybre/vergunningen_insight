import os
import shutil
from datetime import datetime

def backup_project(project_dir, backup_root_dir, folders_to_backup, file_extension=".py"):
    """
    Backs up specified files and folders from the project directory to a backup directory.

    Parameters:
    - project_dir (str): Path to the main project directory.
    - backup_root_dir (str): Path where backup directories will be created.
    - folders_to_backup (list): List of folder names to back up.
    - file_extension (str): File extension to back up from the main directory.
    """
    # Ensure the project directory exists
    if not os.path.isdir(project_dir):
        print(f"Error: The project directory '{project_dir}' does not exist.")
        return

    # Generate a timestamp for the backup folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir_name = f"backup_{timestamp}"
    backup_dir_path = os.path.join(backup_root_dir, backup_dir_name)

    try:
        # Create the backup directory
        os.makedirs(backup_dir_path, exist_ok=False)
        print(f"Created backup directory: '{backup_dir_path}'")
    except Exception as e:
        print(f"Error creating backup directory: {e}")
        return

    # 1. Copy all .py files from the main directory to the backup directory
    try:
        # List all items in the project directory
        for item in os.listdir(project_dir):
            item_path = os.path.join(project_dir, item)
            # Check if it's a file with the specified extension
            if os.path.isfile(item_path) and item.lower().endswith(file_extension.lower()):
                shutil.copy2(item_path, backup_dir_path)
                print(f"Copied file: '{item}'")
    except Exception as e:
        print(f"Error copying .{file_extension} files: {e}")

    # 2. Copy specified folders and their contents to the backup directory
    for folder in folders_to_backup:
        source_folder_path = os.path.join(project_dir, folder)
        destination_folder_path = os.path.join(backup_dir_path, folder)

        if os.path.isdir(source_folder_path):
            try:
                shutil.copytree(source_folder_path, destination_folder_path)
                print(f"Copied folder: '{folder}'")
            except Exception as e:
                print(f"Error copying folder '{folder}': {e}")
        else:
            print(f"Warning: Folder '{folder}' does not exist and will be skipped.")

    print(f"Backup completed successfully to '{backup_dir_path}'.")

if __name__ == "__main__":
    # Define the project directory
    project_directory = r"G:\My Drive\py\Vergunningen-prognose"

    # Define the root directory where backups will be stored
    # You can set this to the same as project_directory or another location
    backup_root_directory = r"G:\My Drive\py\Vergunningen-prognose\Backups"  # Change if needed

    # Define the folders you want to back up
    folders_to_include = ["data", "graphs", "scripts", "static", "template"]

    # Call the backup function
    backup_project(
        project_dir=project_directory,
        backup_root_dir=backup_root_directory,
        folders_to_backup=folders_to_include,
        file_extension=".py"
    )
