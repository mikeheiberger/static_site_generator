import os
import shutil

def copy_directory(source: str, dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if not os.path.exists(source):
        raise ValueError("Incorrect source path")
    os.mkdir(dest)
    source_children = os.listdir(source)
    for child in source_children:
        current_source = os.path.join(source, child)
        current_dest = os.path.join(dest, child)
        if os.path.isfile(current_source):
            shutil.copy(current_source, current_dest)
        else:
            copy_directory(current_source, current_dest)

def main():
    copy_directory("static", "public")

main()