import os
import shutil

def rename_files(directory):
    # Get a list of all files in the specified directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Sort the files in alphabetical order
    files.sort()
    
    # Rename each file according to the desired order
    for index, file_name in enumerate(files, start=0):
        # Create the new file name using the prefix and index
        f=file_name.split('_')
        
        print(f[2].split(".")[0])

# Specify the directory you want to work with
directory = "top250/"

# Call the function to rename the files
rename_files(directory)
