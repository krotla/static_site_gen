import re
from functools import reduce

from markdown import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextType, text_to_textnodes

SPLIT_OL_PATTERN = r"^(?:\d\.\s)"

class HtmlNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        return reduce(lambda str, atr: str + f" {atr[0]}=\"{atr[1]}\"", 
                      self.props.items(), "")
   
    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HtmlNode):

    def __init__(self, tag, value, props=None):
        super(LeafNode,self).__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Leaf node must have value!")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HtmlNode):

    def __init__(self, tag, children, props=None):
        super(ParentNode,self).__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node must have value!")
        if not self.children:
            raise ValueError("Parent node must have at least one child!")
        return f"<{self.tag}{self.props_to_html()}>{"".join([child.to_html() for child in self.children])}</{self.tag}>"
        
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
        
def markdown_to_html_node(md):
    md_blocks = markdown_to_blocks(md)
    html_block_nodes = []
    for md_block in md_blocks:
        md_block_type = block_to_block_type(md_block)
        match(md_block_type):
            case BlockType.CODE:
                md_block = md_block.lstrip("`\n")
                md_block = md_block.rstrip("`")
                html_code_block_node = LeafNode("code", md_block)
                html_block_node = ParentNode("pre", [html_code_block_node])
            case BlockType.PARAGRAPH:
                md_block = " ".join(md_block.splitlines())
                children_html_nodes = markdown_to_children(md_block)                
                html_block_node = ParentNode("p",children_html_nodes)
            case BlockType.HEADING:
                h_tag = heading_block_tag(md_block)
                md_block = md_block.lstrip("# ")
                children_html_nodes = markdown_to_children(md_block)   
                html_block_node = ParentNode(h_tag,children_html_nodes)
            case BlockType.QUOTE:
                md_block_lines = md_block.splitlines()
                md_block = " ".join([line.lstrip(">") for line in md_block_lines])
                children_html_nodes = markdown_to_children(md_block)
                html_block_node = ParentNode("blockquote",children_html_nodes)
            case BlockType.UNORDERED_LIST:
                html_item_nodes = []
                md_ul = md_block.split("- ")
                for md_li in md_ul:
                    if md_li == '':
                        continue
                    md_li = md_li.strip()
                    children_html_li_nodes = markdown_to_children(md_li)
                    html_item_nodes.append(ParentNode("li",children_html_li_nodes))
                html_block_node = ParentNode("ul",html_item_nodes)
            case BlockType.ORDERED_LIST:
                html_item_nodes = []
                md_ol = re.split(SPLIT_OL_PATTERN, md_block, flags=re.MULTILINE)
                for md_li in md_ol:
                    if md_li == '':
                        continue
                    md_li = md_li.strip()
                    children_html_li_nodes = markdown_to_children(md_li)
                    html_item_nodes.append(ParentNode("li",children_html_li_nodes))
                html_block_node = ParentNode("ol",html_item_nodes)
        html_block_nodes.append(html_block_node)
    return ParentNode("div", html_block_nodes)

def markdown_to_children(md):
    html_nodes = []
    text_nodes = text_to_textnodes(md)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def heading_block_tag(md_block):
    heading_chunk = md_block[:6] if len(md_block) > 6 else md_block
    heading_size = heading_chunk.rfind("#") + 1
    return f"h{heading_size}"