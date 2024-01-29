import os as os
import sys
import shutil as sh
from datetime import datetime


def batch_rename(prefix, suffix, replace, replace_with):
    # get list of files in directory

    file_list = [file for file in os.listdir() if file if file != 'file_renamer.py' ]
    for file in file_list:
        base_name, extension = os.path.splitext(file)
        
        # replace words
        base_name = base_name.replace(replace,replace_with)
        
        # add prefix/suffix
        new_name = f'{prefix}{base_name}{suffix}{extension}'
       
        # rename files 
        os.rename(os.path.join(file),os.path.join(new_name))

    return

# user input
if __name__ == "__main__":
    # Prompt user for arguments
    prefix = input("Enter prefix (press Enter for no prefix): ").strip() or ""
    suffix = input("Enter suffix (press Enter for no suffix): ").strip() or ""
    replace = input("Enter text to replace (press Enter for no replacement): ").strip() or ""
    replace_with = input("Enter replacement text (press Enter for no replacement): ").strip() or ""

    # Call batch_rename function with user-provided arguments
    batch_rename(prefix, suffix, replace, replace_with)
