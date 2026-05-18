import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        to_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                generate_page(
                    from_path,
                    template_path,
                    to_path[:-3] + ".html",
                )
        else:
            os.makedirs(to_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, to_path)


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


main()