import os
import shutil


def copy_files_walk(source_path, dest_path):
    #Delete the whole directory if it exist
    #Create a new directory
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
        os.mkdir(dest_path)
    else:
        os.mkdir(dest_path)

    #Using os.walk to find all sub-directories and files
    dir_list = []
    file_list = []
    for root, dirs, files in os.walk(source_path):
        for name in dirs:
            dir_list.append(os.path.join(root,name))
        for name in files:
            file_list.append(os.path.join(root,name))
    
    #Using replace to source path with destination path
    for dir in dir_list:
        new_dir = dir.replace(source_path, dest_path)
        print("Creating " + dir + " to " + dest_path)
        os.mkdir(new_dir)

    for file in file_list:
        new_file = file.replace(source_path, dest_path)
        print("Copying " + file + " to " + dest_path)
        shutil.copy(file, new_file)

