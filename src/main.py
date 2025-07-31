import re

from textnode import TextNode, TextType
from htmlnode import LeafNode

IMG_PATTERN = r"\!\[(.*?)\]\((.*?)\)"
LINK_PATTERN = r"\[(.*?)\]\((.*?)\)"

def main():
    tn = TextNode("Example o a bold text", TextType.BOLD)
    print(tn)

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": f"{text_node.url}", "alt": f"{text_node.text}"})
        case _:
            raise Exception("This TextType does not exist!") 

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
        images = extract_markdown_images(text_to_split)
        for image_alt, image_link in images:            
            sections = text_to_split.split(f"![{image_alt}]({image_link})", 1)
            splitted.append(TextNode(sections[0], TextType.TEXT))
            splitted.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text_to_split = sections[1]
        if text_to_split != '':
            splitted.append(TextNode(text_to_split, TextType.TEXT))
    return splitted

def split_nodes_link(old_nodes):
    pass

def extract_markdown_images(text):    
    matches = re.findall(IMG_PATTERN, text)
    return matches

def extract_markdown_links(text):    
    matches = re.findall(LINK_PATTERN, text)
    return matches

main()