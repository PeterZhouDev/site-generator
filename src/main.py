import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_page

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        to_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                generate_page(
                    from_path,
                    template_path,
                    to_path[:-3] + ".html",
                    basepath,
                )
        else:
            os.makedirs(to_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, to_path, basepath)


def main():
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


main()