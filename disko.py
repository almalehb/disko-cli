import os
import csv
from disko_helpers import *

print_instructions()
dir_path = check_directory_exists()

# we need to check optional filter values
filter_size = check_size_filter()
filter_format = check_file_format_filter()
filter_date = check_date_filter()

# now we can build the CSV file
build_CSV(dir_path, filter_size, filter_format, filter_date)

wait_for_filter()
clean_up_unfiltered_data()


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

os.remove('filtered.csv')
