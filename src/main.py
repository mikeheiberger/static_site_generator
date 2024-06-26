import os
import shutil
from page_generation import generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_template = "./template.html"
dest_dir_path = "./public"

def copy_directory(source: str, dest: str):
    if not os.path.exists(source):
        raise ValueError("Incorrect source path")
    if not os.path.exists(dest):
        os.mkdir(dest)
    for child in os.listdir(source):
        current_source = os.path.join(source, child)
        current_dest = os.path.join(dest, child)
        if os.path.isfile(current_source):
            shutil.copy(current_source, current_dest)
        else:
            copy_directory(current_source, current_dest)

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_directory(dir_path_static, dir_path_public)

    if not os.path.exists(dir_path_content):
        raise ValueError(f"{dir_path_content} does not exist")

    if not os.path.exists(dir_path_template):
        raise ValueError(f"{dir_path_template} does not exist")

    generate_page_recursive(dir_path_content, dir_path_template, dest_dir_path)

main()