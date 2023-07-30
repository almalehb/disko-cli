import os
import csv
from datetime import datetime
import sys
import time

# request path for directory to search inside plus optional filter 
if len(sys.argv) < 2 or len(sys.argv) > 6:
    print("Usage: python file_info.py <directory_path> [min-size <size_in_MB>] [file-format <format>]")
    sys.exit(1)

dir_path = sys.argv[1]
filter_type = None
filter_value = None

# does the directory exist? 
if not os.path.isdir(dir_path):
    print("Directory does not exist!")
    sys.exit(1)

if len(sys.argv) >= 4:
    filter_type_1 = sys.argv[2]
    filter_value_1 = sys.argv[3]
    if filter_type_1 == "min-size":
        filter_size = float(filter_value_1)
    elif filter_type_1 == "file-format":
        filter_format = filter_value_1

if len(sys.argv) == 6:
    filter_type_2 = sys.argv[4]
    filter_value_2 = sys.argv[5]
    if filter_type_2 == "min-size":
        filter_size = float(filter_value_2)
    elif filter_type_2 == "file-format":
        filter_format = filter_value_2

# Let's prepare the CSV file
with open('unfiltered.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # First row has the filter information
    if filter_type and filter_value:
        writer.writerow([f"{filter_type}",f"{filter_value}"])

    # Next row contains the headers
    writer.writerow(["File Name", "Size (MB)", "Date Modified", "File Format", "File Path"])
    
    # Write the filter information
    filter_info = ["null", "null", "null", "null", "null"]
    if filter_size is not None:
        filter_info[1] = f"> {filter_size}"
    if filter_format is not None:
        filter_info[3] = filter_format
    writer.writerow(filter_info)

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
                # file size (megabytes)
                size = round(os.path.getsize(file_path) / (1024 * 1024), 2)
                # last modified date
                date_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                date_modified = date_modified.strftime("%m-%d-%Y %H:%M:%S")
                # file format
                file_format = os.path.splitext(file_path)[1][1:]  # Exclude the first character which is '.'
                # write the data that we have
                writer.writerow([name, size, date_modified, file_format, file_path])
            except Exception as e:
                print(f"Can't get info for file {file_path}! Error: {str(e)}")

# Now we wait for the microservice to finish its filtering work, which would output filtered.csv 
while not os.path.exists('filtered.csv'):
    time.sleep(1)

# We don't need unfiltered.csv anymore
if os.path.exists('unfiltered.csv'):
    os.remove('unfiltered.csv')

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
