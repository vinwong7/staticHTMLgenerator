from copystatic import copy_files_walk
from generate_page import generate_page_recursive


def main():
    static_path = "./static"
    public_path = "./public"
  
    copy_files_walk(static_path, public_path)

    generate_page_recursive("./content", "template.html", "./public")


main()