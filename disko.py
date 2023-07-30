import os
import csv
from datetime import datetime
import mimetypes
import sys
import time

# request path for directory to search inside
if len(sys.argv) != 2:
    print("How to use: python disko.py <directory_path>")
    sys.exit(1)

dir_path = sys.argv[1]

# does the directory exist? 
if not os.path.isdir(dir_path):
    print("Directory does not exist!")
    sys.exit(1)

# Let's prepare the CSV file
with open('search_results.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # First row contains the headers
    writer.writerow(["File Name", "Size (Bytes)", "Date Modified", "File Format", "File Path"])
    
    # Let's walk through the directory, recursively
    for root, directories, files in os.walk(dir_path):

        # We should ignore hidden directories, remove them from directories list
        directories[:] = [directory for directory in directories if not directory[0] == '.']
        
        for name in files:
            # We shoudl also ignore hidden files
            if name.startswith('.'):
                continue

            file_path = os.path.join(root, name)
            
            try:
                # file size
                size = os.path.getsize(file_path)
                # last modified date
                date_modified = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                # file format
                file_format = mimetypes.guess_type(file_path)[0]
                # write the data that we have
                writer.writerow([name, size, date_modified, file_format, file_path])
            except Exception as e:
                print(f"Can't get info for file {file_path}! Error: {str(e)}")

# Now we wait for the microservice to finish its filtering work, which would output filtered.csv 
while not os.path.exists('filtered.csv'):
    time.sleep(1)

# We don't need search_results.csv anymore
if os.path.exists('search_results.csv'):
    os.remove('search_results.csv')

# Let's print out the contents of filtered.csv, in a somewhat structured way (keep columns aligned)
# We need to figure out the maximum length of all fields
all_rows = []
max_lens = []
with open('filtered.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        all_rows.append(row)
        if not max_lens:
            max_lens = [len(field) for field in row]
        else:  
            max_lens = [max(max_lens[i], len(field)) for i, field in enumerate(row)]

# Finally, print out the contents of filtered.csv in a tabular format
for row in all_rows:
    print(' '.join('%%-%ds' % max_lens[i] % field for i, field in enumerate(row)))