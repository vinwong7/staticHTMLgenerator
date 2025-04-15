from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    final_list = []
    markdown = markdown.strip()
    markdown_list = markdown.split("\n\n")
    for i in range(len(markdown_list)):
        block = markdown_list[i].strip()
        if block != "":
            final_list.append(block)
    return final_list

def block_to_block_type(markdown):
    headings_list = ["# ", "## ", "### ", "#### ","##### ", "###### "]
    for i in range(len(headings_list)):
        if headings_list[i] == markdown[:i+2]:
            return BlockType.HEADING
    if markdown[:3] == "```" and markdown[-3:] == "```":
        return BlockType.CODE
    
    lines_list = markdown.split("\n")
    quote_check = True
    for i in lines_list:
        if i[0] != ">":
            quote_check = False
    if quote_check == True:
        return BlockType.QUOTE
    
    unordered_list_check = True
    for i in lines_list:
        if i[:2] != "- ":
            unordered_list_check = False
    if unordered_list_check == True:
        return BlockType.ULIST
    
    ordered_list_check = True
    for i in range(len(lines_list)):
        if lines_list[i][:3] != str(i+1) + ". ":
            ordered_list_check = False
    if ordered_list_check == True:
        return BlockType.OLIST

    return BlockType.PARAGRAPH