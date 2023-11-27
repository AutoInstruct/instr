import msvcrt
import serial

# Configure the serial port
port = 'COM3'
baudrate = 57600
timeout = 1

# Open the serial port
ser = serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity='N', stopbits=1, timeout=timeout)


while True:
    
    data = ser.readline#.decode('latin-1')
    print(data)
    key = msvcrt.getch()
    
    if key == 'q':
        break

    
