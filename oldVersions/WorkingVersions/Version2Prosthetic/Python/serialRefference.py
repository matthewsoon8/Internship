from serial.tools import list_ports
import serial
import time
import csv

# Identify the correct port
ports = list_ports.comports()
for port in ports: print(port)

# Create CSV file
f = open("data.csv","w",newline='')
f.truncate()

# Open the serial com
serialCom = serial.Serial('COM5',9600)

# Toggle DTR to reset the Arduino
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

# How many data points to record
kmax = 50

# Loop through and collect data as it is available
for k in range(kmax):
    
    try:
        # Read the line
        s_bytes = serialCom.readline()
        time.sleep(0.05)
        decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
        print(decoded_bytes)

        # Parse the line
        values = decoded_bytes.split(",")

        print(values)

        # Write to CSV
        writer = csv.writer(f,delimiter=",")
        writer.writerow(values)
        #time.sleep(1)
    except:
        print("Error encountered, line was not recorded.")

    serialCom.flushInput()

f.close()