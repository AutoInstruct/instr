import csv

def extract_values(input_string):
    values = {}
    # Assuming the input string format remains constant
    parts = input_string.split()
    values['SERN'] = parts[1].lstrip("b'\rSN:")
    values['DATE'] = parts[2]
    values['TIME'] = parts[3]
    values['MODE'] = parts[4]
    values['DURA'] = parts[5].rstrip("sec")
    values['ANGL'] = parts[6].rstrip("degrees")
    values['SCRW'] = parts[7].lstrip("Screw:")
    values['ERRO'] = parts[8].split('/')[0].lstrip("Errors:")
    values['PROG'] = parts[9].lstrip("Prog:")
    values['TORQ'] = parts[10].lstrip("Torque:").rstrip("Nm")
    values['SEQE'] = parts[11].lstrip("Seq:").rstrip("\n")

    return values



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
    
    
receivedstring = "b'\rSN:2308566 2023/10/07 18:29:31 REV 1.17sec 5763degrees Screw:00/05 Errors:00/02 Prog:01 Torque:0.00/1.00Nm Seq:Off\n'"
filepath = 'C:/Users/Christian/Desktop/MECCATRONICA/Tesi/codetests/comread/test_data.csv'


stringtocsv(receivedstring, filepath)
