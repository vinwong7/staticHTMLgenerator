import os
import shutil
from block_markdown import markdown_to_html_node
from htmlnode import ParentNode

def extract_title(markdown):
    block_list = markdown.split("\n\n")
    header = ""
    for block in block_list:
        if block.startswith("# "):
            header = block
            break
    if header == "":
        raise Exception("No h1 header found.")
    else:
        header_text = header[2:]
        header_text = header_text.strip()
    return header_text    

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")

    md_file = open(from_path, "r")
    md = md_file.read()

    template_file = open(template_path, "r")
    template = template_file.read()

    md_html = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", md_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_path_dir = os.path.dirname(dest_path)
    if os.path.exists(dest_path_dir) is False:
        os.makedirs(dest_path_dir)
    
    f = open(dest_path, "w")
    f.write(template)
    
    f.close()
    md_file.close()
    template_file.close()


def generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path,filename)

        if os.path.isfile(from_path):
            html_name = dest_path[:-2] + "html"
            generate_page(from_path, template_path, html_name, basepath)
        else:
            generate_page_recursive(from_path, template_path, dest_path, basepath)
