import os
import shutil

def copy_directory_recursive(src_dir, dest_dir):
    """
    Recursively loops through src_dir and copies everything to dest_dir.
    Assumes the base target folder structure is managed by the caller.
    """
    # If a nested subdirectory doesn't exist yet, create it
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            print(f"  -> File: {src_path} to {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"  -> Entering Directory: {src_path}")
            # Recurse down one level deeper
            copy_directory_recursive(src_path, dest_path)