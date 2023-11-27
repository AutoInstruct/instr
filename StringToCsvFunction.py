import csv

#This function takes data strings from electric screwdrivers and appends them to a csv file
#It makes use of the extract_values function to label the first row with the data keys
#The arguments are the string to append and the path to thecsv file


def stringtocsv(datastring, csvpath):
    # Extract values
    data_values = extract_values(datastring)

    # Write to CSV file
    with open(csvpath, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data_values.keys())

        # If the file is empty, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the data
        writer.writerow(data_values)

