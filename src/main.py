from textnode import TextNode, TextType
import os
import shutil
from copystatic import copy_directory_recursive

def main():
    # Creating a dummy TextNode instance
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    # Printing the object to see the __repr__ output
    print(node)

    source_dir = "static"
    target_dir = "public"

    # Step 1: If destination exists, remove it completely
    if os.path.exists(target_dir):
        print(f"Cleaning up old target directory: '{target_dir}'...")
        shutil.rmtree(target_dir)
    
    # Step 2: Recreate the base target folder fresh
    print(f"Creating fresh target directory: '{target_dir}'...")
    os.mkdir(target_dir)
    
    # Step 3: Copy source directory into destination recursively
    print(f"Beginning asset copy from '{source_dir}' to '{target_dir}'...")
    copy_directory_recursive(source_dir, target_dir)
    print("Asset synchronization complete!")

if __name__ == "__main__":
    main()# hello world
