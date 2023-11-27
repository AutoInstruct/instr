
#This function extracts values from the string provided as argument.
#The argument string should be the one read from the COM port connected to the smart screwdriver
#The input string should have the following structure/content e.g. : b'\rSN:2308566 2023/10/07 18:28:32 REV 1.22sec 5981degrees Screw:00/05 Errors:00/02 Prog:01 Torque:0.00/1.00Nm Seq:Off\n'
#The extracted values are put in a dictionary with an appropriate four letter string as a key

def extract_values(input_string):
    values = {}
    # Assuming the input string format remains constant
    parts = input_string.split()
    values['SERN'] = parts[1].lstrip("b'\\rSN:")
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