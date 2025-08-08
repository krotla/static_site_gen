import os
import shutil

from markdown import BlockType, markdown_to_blocks, block_to_block_type, extract_title
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, markdown_to_html_node


def main():
    try:
        clean_and_copy("./static", "./public")
        generate_page("content/index.md", "template.html", "public/index.html")
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

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path) as md_file:
            md = md_file.read()
        with open(template_path) as template_file:
            template = template_file.read()
        html_content_node = markdown_to_html_node(md)
        html_content = html_content_node.to_html()
        title = extract_title(md)
        html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
        dest_dir_path = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
        with open(dest_path,"w") as html_file:
            html_file.write(html_page)
    except Exception as e:
        print(e)

main()