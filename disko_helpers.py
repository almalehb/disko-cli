import os
import csv
from datetime import datetime
import sys
import time


def print_instructions():
    if len(sys.argv) < 2:
        print("Usage: python disko.py <directory_path> [min-size <size_in_MB>] [file-format <format>] [newer-than <date>]")
        sys.exit(1)


def check_directory_exists(): 
    dir_path = sys.argv[1]

    if not os.path.isdir(dir_path):
        print("Directory does not exist!")
        sys.exit(1)
    return dir_path


def get_filter_value(filter_type):
    """Helper function to retrieve filter value based on its type"""
    if filter_type in sys.argv:
        arg_index = sys.argv.index(filter_type) + 1
        if arg_index < len(sys.argv):
            return sys.argv[arg_index]
    return None


def check_size_filter(): 
    filter_size = get_filter_value('min-size')
    if filter_size:
        filter_size = float(filter_size)
    return filter_size


def check_file_format_filter(): 
    return get_filter_value('file-format')


def check_date_filter():
    filter_date = get_filter_value('newer-than')
    if filter_date:
        filter_date = datetime.strptime(filter_date, "%m/%d/%Y %H:%M:%S")
    return filter_date


def build_filter_information(filter_size, filter_format, filter_date): 
    filter_info = ["null", "null", "null", "null", "null"]
    if filter_size is not None:
        filter_info[1] = f"> {filter_size}"
    if filter_format is not None:
        filter_info[3] = filter_format
    if filter_date is not None:
        formatted_date = filter_date.strftime("%m/%d/%Y %H:%M:%S")
        filter_info[2] = f"> {formatted_date}"
    return filter_info


def build_directory_data(root, dirs, files):
    dirs[:] = [d for d in dirs if not d[0] == '.'] # Ignore hidden directories

    for name in files:
        if name.startswith('.'): # also, ignore hidden files
            continue

        file_path = os.path.join(root, name)
        
        try:
            # file size in MB, rounded to two decimal places
            size = round(os.path.getsize(file_path) / (1024 * 1024), 2)
            # last modified date (incl. formatting, per contract)
            date_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
            date_modified_str = date_modified.strftime("%m/%d/%Y %H:%M:%S")
            # get file extension
            file_format = os.path.splitext(file_path)[1][1:]  
            return [name, size, date_modified_str, file_format, file_path]
        except Exception as e:
            print(f"Cannot get info for file {file_path}. Error: {str(e)}")
            return None 


def build_CSV(dir_path, filter_size, filter_format, filter_date): 
    with open('unfiltered.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # start with the headers
        writer.writerow(["File Name", "Size (MB)", "Date Modified", "File Format", "File Path"])

        # next, add the filter information
        filter_info = build_filter_information(filter_size, filter_format, filter_date)
        writer.writerow(filter_info)
        
        # let's walk through directory
        for root, dirs, files in os.walk(dir_path):
            data = build_directory_data(root, dirs, files)
            if data is not None: 
                writer.writerow(data) # write the data to the CSV file


def wait_for_filter():
    while not os.path.exists('filtered.csv'):
        time.sleep(1)


def clean_up_unfiltered_data():
    if os.path.exists('unfiltered.csv'):
        os.remove('unfiltered.csv')

