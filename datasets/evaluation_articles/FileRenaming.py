import os

# Set the directory where your files are located
directory = 'articles'

# Loop through the files in the directory
for filename in os.listdir(directory):
    if filename.startswith('doc_') and filename.endswith('.txt'):
        # Split the filename on underscores and periods to isolate x and y
        parts = filename.split('_')
        if len(parts) == 3 and parts[2].endswith('.txt'):
            # Construct the new filename
            new_filename = f"{parts[0]}_{parts[1]}.txt"
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f'Renamed {filename} to {new_filename}')

print('Renaming complete.')
