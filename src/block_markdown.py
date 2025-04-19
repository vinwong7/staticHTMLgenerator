from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

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
        block = markdown_list[i]
        block = block.strip()
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

def text_to_children(text):
    #Convert text into a list of text nodes
    children_text_nodes = text_to_textnodes(text)
    children_html_list = []
    #Go through each text node and convert into html nodes, then append to list
    for node in children_text_nodes:
        child_html_node = text_node_to_html_node(node)
        children_html_list.append(child_html_node)
    return children_html_list

def paragraph_node(block):
    #Base node for paragraph has p tag and blank children
    base_node = ParentNode("p", [])
    #New lines do not matter, so rejoin them with space
    block_text = " ".join(block.split("\n"))
    #Use text to children function to create children HTML nodes from text
    base_node.children = text_to_children(block_text)
    return base_node


def header_node(block):
    base_node_list = []
    #Potentially have multiple headers, split all lines by newline
    #then redo lines depending on if there is a header marker
    lines = block.split("\n")
    redone_lines = []
    line_check = ""
    for line in lines:
        if line_check == "" and line[0] == "#":
            line_check = line
        elif len(line) == 0:
            continue
        elif line[0] != "#":
            line_check += " " + line
        elif line[0] == "#":
            redone_lines.append(line_check)
            line_check = line
    redone_lines.append(line_check)

    #Using each line, create base node and strip header character off
    #Base node for header is dependent on amount of #
    for redone_line in redone_lines:
        if redone_line.startswith("# "):
            base_node = ParentNode("h1", [])
            text = redone_line.strip("# ")
        elif redone_line.startswith("## "):
            base_node = ParentNode("h2", [])
            text = redone_line.strip("## ")
        elif redone_line.startswith("### "):
            base_node = ParentNode("h3", [])
            text = redone_line.strip("### ")
        elif redone_line.startswith("#### "):
            base_node = ParentNode("h4", [])
            text = redone_line.strip("#### ")
        elif redone_line.startswith("##### "):
            base_node = ParentNode("h5", [])
            text = redone_line.strip("##### ")
        elif redone_line.startswith("###### "):
            base_node = ParentNode("h6", [])
            text = redone_line.strip("###### ")
        else:
            raise Exception("not a header")

        base_node.children = text_to_children(text)
        base_node_list.append(base_node)
    return base_node_list

def quote_node(block):
    #Base node for paragraph has blockquote tag and blank children
    base_node = ParentNode("blockquote", [])
    #New lines do not matter, so rejoin them with space; 
    #Quote blocks always have > in front, so include that in the split
    block_text = " ".join(block.split("\n>"))
    #beginning text wouldn't have the new line, so take it out manually
    block_text = block_text[1:]
    block_text = block_text.strip()
    base_node.children = text_to_children(block_text)
    return base_node

def code_node(block):
    #Base node for paragraph has blockquote tag and blank children
    final_node = ParentNode("pre", [])
    base_node = ParentNode("code", [])
    #Remove code block indicators ```
    block = block.strip("\n")
    block_text = block[3:-3]
    #Code blocks do not need inline conversion; take block text as is
    text_node = TextNode(block_text, TextType.TEXT)
    base_node.children = [text_node_to_html_node(text_node)]
    final_node.children = [base_node]
    return final_node

def ulist_node(block):
    line_item_node_list = []
    line_item_list = block.split("\n")
    for line_item in line_item_list:
        text = line_item[2:]
        child_html_node = text_to_children(text)
        line_item_node = ParentNode("li", child_html_node)
        line_item_node_list.append(line_item_node)
    final_node = ParentNode("ul", line_item_node_list)
    return final_node

def olist_node(block):
    line_item_node_list = []
    line_item_list = block.split("\n")
    for line_item in line_item_list:
        text = line_item[3:]
        child_html_node = text_to_children(text)
        line_item_node = ParentNode("li", child_html_node)
        line_item_node_list.append(line_item_node)
    final_node = ParentNode("ol", line_item_node_list)
    return final_node

def markdown_to_html_node(markdown):
    html_node_list = []
    blocks_list = markdown_to_blocks(markdown)
    for block in blocks_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            parent_node = paragraph_node(block)
        elif block_type == BlockType.HEADING:
            parent_node = header_node(block)
        elif block_type == BlockType.QUOTE:
            parent_node = quote_node(block)
        elif block_type == BlockType.CODE:
            parent_node = code_node(block)
        elif block_type == BlockType.ULIST:
            parent_node = ulist_node(block)
        elif block_type == BlockType.OLIST:
            parent_node = olist_node(block)
        
        if type(parent_node) is list:
            html_node_list.extend(parent_node)
        else:
            html_node_list.append(parent_node)
    
    final_parent_node = ParentNode("div", html_node_list)


    return final_parent_node