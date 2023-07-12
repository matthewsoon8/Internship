from serial.tools import list_ports
import serial
import time
import csv

# Identify the correct port
ports = list_ports.comports()
for port in ports:
    print(port)

# Create CSV file
f = open("data.csv", "w", newline='')
f.truncate()

# Open the serial com
serialCom = serial.Serial('COM42', 9600)

# Toggle DTR to reset the Arduino
serialCom.setDTR(False)
time.sleep(1)
serialCom.flushInput()
serialCom.setDTR(True)

# How many data points to record
kmax = 50

# Skip initial values
for _ in range(10):
    serialCom.readline()

# Loop through and collect data as it is available
for k in range(kmax):
    #serialCom.flushInput()
    try:
        # Read the line
        s_bytes = serialCom.readline()
        decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')
        print(decoded_bytes)

        # Parse the line
        if k % 20 == 0:  # Read one value every 20 iterations (1 value per second assuming 20 values per second from Arduino)     
            values = decoded_bytes.split(",")
            print(values)

            # Write to CSV
            #writer = csv.writer(f, delimiter=",")
            #writer.writerow(values)
        time.sleep(0.05)  # Add a small delay between iterations
    except:
        print("Error encountered, line was not recorded.")
        serialCom.flushInput()
f.close()
