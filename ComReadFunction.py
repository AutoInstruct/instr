import serial


#This function reads data from one or three COM ports, the arguments are the name(s) of the port(s)
#Give onle one argument if only one port needs to be read
#The function returns the strings read from the COM ports


def com_read(com1, com2, com3):
#COM COM ports configuration
    comport1 = com1
    comport2 = com2
    comport3 = com3
    baudrate = 57600
    timeout = 1
    #Open COM ports
    ser1 = serial.Serial(port=comport1, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=timeout)
    if comport2 and comport3:
        ser2 = serial.Serial(port=comport2, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=timeout)
        ser3 = serial.Serial(port=comport3, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=timeout)
    #COM Read data from COM ports
    in_com1 = ser1.readline()
    if comport2 and comport3:
        in_com2 = ser2.readline()
        in_com3 = ser3.readline()
    # Close the COM ports
    ser1.close()
    if comport2 and comport3:
        ser2.close()
        ser3.close()
    
    if comport2 and comport3:   
        return in_com1 , in_com2 , in_com3
    else:
        return in_com1