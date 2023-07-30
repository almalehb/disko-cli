import os
import csv
from datetime import datetime
import sys
import time

def get_filter_value(filter_type):
    """helper function to help us retrieve filter value based on its type"""
    if filter_type in sys.argv:
        arg_index = sys.argv.index(filter_type) + 1
        if arg_index < len(sys.argv):
            return sys.argv[arg_index]
    return None

# request path for directory to search inside plus optional filter 
if len(sys.argv) < 2:
    print("Usage: python disko.py <directory_path> [min-size <size_in_MB>] [file-format <format>] [newer-than <date>]")
    sys.exit(1)

dir_path = sys.argv[1]

# first let's check if directory exists
if not os.path.isdir(dir_path):
    print("Directory does not exist!")
    sys.exit(1)

# we need to check optional filter values
filter_size = get_filter_value('min-size')
if filter_size:
    filter_size = float(filter_size)

filter_format = get_filter_value('file-format')

filter_date = get_filter_value('newer-than')
if filter_date:
    filter_date = datetime.strptime(filter_date, "%m/%d/%y %H:%M:%S")

# now we can build the CSV file
with open('unfiltered.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # start with the headers
    writer.writerow(["File Name", "Size (MB)", "Date Modified", "File Format", "File Path"])
    
    # next, add the filter information
    filter_info = ["null", "null", "null", "null", "null"]
    if filter_size is not None:
        filter_info[1] = f"> {filter_size}"
    if filter_format is not None:
        filter_info[3] = filter_format
    if filter_date is not None:
        filter_info[2] = f"> {filter_date}"
    writer.writerow(filter_info)
    
    file_data = []  # List to store the data of all files
    
    # let's walk through directory
    for root, dirs, files in os.walk(dir_path):
        # Be sure to ignore hidden directories
        dirs[:] = [d for d in dirs if not d[0] == '.']
        
        for name in files:
            # also, ignore hidden files
            if name.startswith('.'):
                continue

            file_path = os.path.join(root, name)
            
            try:
                # file size in MB, rounded to two decimal places
                size = round(os.path.getsize(file_path) / (1024 * 1024), 2)
                # last modified date (incl. formatting, per contract)
                date_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                date_modified_str = date_modified.strftime("%m-%d-%Y %H:%M:%S")
                # get file extension
                file_format = os.path.splitext(file_path)[1][1:]  
                # store all that data
                file_data.append([name, size, date_modified_str, file_format, file_path])
            except Exception as e:
                print(f"Cannot get info for file {file_path}. Error: {str(e)}")
    
    # write the data to the CSV file
    for data in file_data:
        writer.writerow(data)

# waiting for filtered.csv to appear
while not os.path.exists('filtered.csv'):
    time.sleep(1)

# delete unfiltered.csv
if os.path.exists('unfiltered.csv'):
    os.remove('unfiltered.csv')

# check the contents of filtered.csv, compute the maximum length of each column (just to have things look pretty, probably unnecessary)
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

# print out the contents of filtered.csv in a tabular format
for row in all_rows:
    print(' '.join('%%-%ds' % max_lens[i] % field for i, field in enumerate(row)))
