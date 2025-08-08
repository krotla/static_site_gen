import re
from enum import Enum

IMG_PATTERN = r"\!\[(.*?)\]\((.*?)\)"
LINK_PATTERN = r"(?<!\!)\[(.*?)\]\((.*?)\)"

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_image(text_nodes)
    return text_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    splitted = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            splitted.append(old_node)
            continue
        splited_texts = old_node.text.split(delimiter)
        if len(splited_texts) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax! Odd number of {delimiter} delimiters.")
        for i, text in enumerate(splited_texts):               
            if i % 2 == 0:
                if text == '':
                    continue
                new_node = TextNode(text, TextType.TEXT)
            else:
                new_node = TextNode(text, text_type)
            splitted.append(new_node)

    return splitted

def split_nodes_image(old_nodes):
    splitted = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            splitted.append(old_node)
            continue
        
        text_to_split = old_node.text
        images = _extract_markdown_images(text_to_split)
        for image_alt, image_link in images:            
            sections = text_to_split.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != '':
                splitted.append(TextNode(sections[0], TextType.TEXT))
            splitted.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_to_split = sections[1]

        if text_to_split != '':
            splitted.append(TextNode(text_to_split, TextType.TEXT))
    return splitted

def _extract_markdown_images(text):    
    matches = re.findall(IMG_PATTERN, text)
    return matches

def split_nodes_link(old_nodes):
    splitted = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            splitted.append(old_node)
            continue
        text_to_split = old_node.text
        links = _extract_markdown_links(text_to_split)
        for name, link in links:            
            sections = text_to_split.split(f"[{name}]({link})", 1)
            splitted.append(TextNode(sections[0], TextType.TEXT))
            splitted.append(TextNode(name, TextType.LINK, link))
            text_to_split = sections[1]
        if text_to_split != '':
            splitted.append(TextNode(text_to_split, TextType.TEXT))
    return splitted

def _extract_markdown_links(text):    
    matches = re.findall(LINK_PATTERN, text)
    return matches