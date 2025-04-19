from copystatic import copy_files_walk
from generate_page import generate_page_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        

    static_path = "./static"
    docs_path = "./docs"
  
    copy_files_walk(static_path, docs_path)

    generate_page_recursive("./content", "template.html", docs_path, basepath)


main()