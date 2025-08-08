import os
import shutil

from markdown import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode


def main():
    try:
        clean_and_copy("./static", "./public")
    except Exception as e:
        print(e)

def clean_and_copy(source, destination):
    check_dir(source)
    check_dir(destination)
    remove_dir_items(destination)
    copy_dir(source, destination)

def check_dir(dir_path):
    dir_name = os.path.dirname(dir_path)
    if not os.path.exists(dir_path):
        raise FileExistsError(f"'{dir_name}' directory does not exist!")
    if not os.path.isdir(dir_path):
        raise NotADirectoryError(f"'{dir_name}' is not a directory!")


def remove_dir_items(path, keep_this = True):
    if os.path.isdir(path):
        dir_content = os.listdir(path)
        for item in dir_content:
            item_path = os.path.join(path, item)
            remove_dir_items(item_path, False)
        if not keep_this:
            os.rmdir(path)
    else:
        os.remove(path)
    

def copy_dir(source, destination):
    source_content = os.listdir(source)        
    for item in source_content:
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isdir(src_path):            
            os.mkdir(dest_path)
            copy_dir(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)


main()