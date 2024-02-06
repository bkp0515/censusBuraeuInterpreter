import csv
import glob
import os
from itertools import islice

def open_metadata_csv():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    metadata_file_pattern = os.path.join(script_directory, "*Metadata.csv")
    data_file_pattern = os.path.join(script_directory, "*Data.csv")

    # Find matching Metadata.csv file
    matching_metadata_files = glob.glob(metadata_file_pattern)

    if matching_metadata_files:
        # Assuming there is only one matching file, you can modify this part accordingly
        metadata_file_path = matching_metadata_files[0]

        with open(metadata_file_path, 'r') as metadata_csv_file:
            metadata_csv_reader = csv.reader(metadata_csv_file)
            
            # Display row numbers along with the second column of the rows (excluding those with "Margin of Error")
            for i, row in enumerate(metadata_csv_reader, start=1):
                if "Margin of Error" not in row[1]:
                    print(f"{i}. {row[1]}")
            
            # Prompt user to select a row
            selected_row = input("Enter the row number you want to select (0 to exit): ")
            
            try:
                selected_row = int(selected_row)
                if 0 < selected_row <= i:
                    # Reopen the metadata file to retrieve the entire row
                    with open(metadata_file_path, 'r') as metadata_csv_file:
                        metadata_csv_reader = csv.reader(metadata_csv_file)
                        selected_row_data = next(islice((row for row in metadata_csv_reader if "Margin of Error" not in row[1]), selected_row - 1, None))
                    
                    print(f"Selected row: {selected_row}. Second column: {selected_row_data[1]}")

                    # Search for the corresponding column in another Data.csv file
                    matching_data_files = glob.glob(data_file_pattern)

                    if matching_data_files:
                        data_file_path = matching_data_files[0]

                        with open(data_file_path, 'r') as data_csv_file:
                            data_csv_reader = csv.reader(data_csv_file)
                            header = next(data_csv_reader)  # Assuming the first row is the header

                            try:
                                column_index = header.index(selected_row_data[0])

                                # Print the data in the first column of the data file and the found column with comma separators
                                for data_row in data_csv_reader:
                                    print(f"{data_row[0]}, {data_row[column_index]}")

                            except ValueError:
                                print(f"Column '{selected_row_data[0]}' not found in {data_file_path}")

                    else:
                        print(f"No file matching the pattern *Data.csv found in the script directory.")
                
                elif selected_row == 0:
                    print("Exiting.")
                else:
                    print("Invalid row number.")
            except ValueError:
                print("Invalid input. Please enter a valid row number.")
    else:
        print("No file matching the pattern *Metadata.csv found in the script directory.")

# Example usage:
open_metadata_csv()
