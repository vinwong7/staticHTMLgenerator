from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        segments = node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise Exception("No closing delimiter found; Invalid Markdown syntax")
        for i in range(len(segments)):
            if segments[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(segments[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(segments[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            delimiter = f"![{image_alt}]({image_link})"
            text_list = original_text.split(delimiter,1)
            if text_list[0] != "":
                new_nodes.append(TextNode(text_list[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            original_text = text_list[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            link_text = link[0]
            link_url = link[1]
            delimiter = f"[{link_text}]({link_url})"
            text_list = original_text.split(delimiter,1)
            if text_list[0] != "":
                new_nodes.append(TextNode(text_list[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = text_list[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]
    text_node = split_nodes_delimiter(text_node, "**", TextType.BOLD)
    text_node = split_nodes_delimiter(text_node, "_", TextType.ITALIC)
    text_node = split_nodes_delimiter(text_node, "`", TextType.CODE)
    text_node = split_nodes_image(text_node)
    text_node = split_nodes_link(text_node)


    return text_node