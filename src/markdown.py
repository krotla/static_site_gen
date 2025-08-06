import re
from enum import Enum

MD_HEADING_PATTERN = r"^(#{1,6})\s{1}(.*?)\s*$"
MD_CODE_PATTERN = r"(^```\n)([\s\S]*?)(^```$)"
MD_QUOTE_PATTERN = r"^((>{1})(.*)(\n*))+"
MD_UNORDERED_LIST_PATTERN = r"^((-{1}\s)(.*)(\n?))+"
MD_ORDERED_LIST_PATTERN = r"(^(\d{1,}\.\s)(.*)(\n?))+"

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown):
    blocks = list(map(str.strip, markdown.split("\n\n")))
    for block in blocks[:]:        
        if block == "":
            blocks.remove(block)
    return blocks

def block_to_block_type(text_block):
    heading_match =  re.findall(MD_HEADING_PATTERN, text_block)
    if heading_match:
        return BlockType.HEADING
    
    #FIXME Find correct regex
    # code_match =  re.match(MD_CODE_PATTERN, text_block)
    code_match = text_block.startswith("```") and text_block.endswith("\n```")
    if code_match:
        return BlockType.CODE
    
    quote_match =  re.findall(MD_QUOTE_PATTERN, text_block)
    if quote_match:
        return BlockType.QUOTE
    
    unordered_list_match =  re.findall(MD_UNORDERED_LIST_PATTERN, text_block)
    if unordered_list_match:
        return BlockType.UNORDERED_LIST
    
    ordered_list_match =  re.findall(MD_ORDERED_LIST_PATTERN, text_block)
    if ordered_list_match:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH