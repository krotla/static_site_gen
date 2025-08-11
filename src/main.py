import sys
import os
import shutil

from markdown import BlockType, markdown_to_blocks, block_to_block_type, extract_title
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, markdown_to_html_node


def main():
    basepath = "/" if len(sys.argv) != 2 else sys.argv[1] 

    try:
        clean_and_copy("static/", "docs/")
        generate_page_recursiv("content/", "template.html", "docs/", basepath)
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

def generate_page_recursiv(dir_path_content, template_path, dest_dir_path, basepath):
    content_paths = list_dir_content_paths(dir_path_content)
    for md_path in content_paths:
        filename, file_extension = os.path.splitext(md_path)
        if file_extension != '.md':
            continue
        html_path = md_path.replace(dir_path_content, dest_dir_path, 1)[:-3] + ".html"
        generate_page(md_path, template_path, html_path, basepath)
    

def list_dir_content_paths(dir):
    dir_content = []
    current_dir = os.listdir(dir)
    for item in current_dir:
        item_path = os.path.join(dir, item)
        if os.path.isdir(item_path):
            subdir_content = list_dir_content_paths(item_path)
            dir_content.extend(subdir_content)
        else:
            dir_content.append(item_path)
    return dir_content


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path) as md_file:
            md = md_file.read()
        with open(template_path) as template_file:
            template = template_file.read()
        html_content_node = markdown_to_html_node(md)
        html_content = html_content_node.to_html()
        title = extract_title(md)
        html_page = template \
            .replace("{{ Title }}", title) \
            .replace("{{ Content }}", html_content) \
            .replace('href="/', f'href="{basepath}') \
            .replace('src="/', f'src="{basepath}')
        dest_dir_path = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir_path):
            os.makedirs(dest_dir_path)
        with open(dest_path,"w") as html_file:
            html_file.write(html_page)
    except Exception as e:
        print(e)

main()