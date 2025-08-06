from markdown import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode


def main():
    tn = TextNode("Example o a bold text", TextType.BOLD)
    print(tn)


main()