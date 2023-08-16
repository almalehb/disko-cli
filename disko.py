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

# compute max length for each column to print a neatly aligned table
all_rows, max_lengths = retrieve_rows_and_lengths()
pretty_print_rows(all_rows, max_lengths)


