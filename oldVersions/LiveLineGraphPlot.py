import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import pandas as pd
import re


indexList=[]
thumbList=[]
pinkyList=[]

def animate(i, pinkyList, ser):
    global indexList
    global thumbList

    ser.write(b'g')                                     # Transmit the char 'g' to the Arduino so it knows to send data
    arduinoData_string = ser.readline().decode('ascii') # recieved value from the arduino
    
    splitData=arduinoData_string.split(",")                 #Split data oncommas [index],[Thumb],[Pinky]
    
    val1 = splitData[0]
    val2 = splitData[1]
    val3 = splitData[2]

    print(float(splitData[2]))

    #print(i)                                           # 'i' is a incrementing variable based upon frames = x argument

    try:
        #individually add each datapoint to the list
        arduinoVal1 = float(val1)                   # Convert to float
        indexList.append(arduinoVal1)              # add each point to its corrosponding list

        arduinoVal2= float(val2)
        pinkyList.append(arduinoVal2)

        arduinoVal3= float(val3)
        thumbList.append(arduinoVal3)

    except:                                             # Pass if data point is bad                               
        pass
    
    #Graph Settings
    ax.clear()                                          # Clear last data frame
    ax.plot(pinkyList)                                   # Plot new data frame

    ax.plot(indexList)

    ax.plot(thumbList)
    
    #ax.set_ylim([0, 15])                                # Set Y axis limit of plot
    ax.set_title("Arduino Data")                        # Set title of figure
    ax.set_ylabel("Value")                              # Set title of y axis 

dataList = []                                           # Create empty list variable for later use
                                                        
fig = plt.figure()                                      # Create Matplotlib plots fig is the 'higher level' plot window
ax = fig.add_subplot(111)                               # Add subplot to main fig window

ser = serial.Serial("COM42", 9600)                       # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
time.sleep(2)                                           # Time delay for Arduino Serial initialization 

                                                    # Matplotlib Animation Fuction that takes takes care of real time plot.
                                                        # Note that 'fargs' parameter is where we pass in our dataList and Serial object. 
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(pinkyList, ser), interval=100) 

plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed
ser.close()                                             # Close Serial connection when plot is closed

#ani.save("livegraph.mp4", writer='ffmpeg')
print(indexList)
print(pinkyList)
print(thumbList)



############################################################################################################
def write_to_excel(dataA,dataB,dataC):

    try:                        # Try to read the existing file
        originalFrame = pd.read_excel('data.xlsx', engine='openpyxl')       #contents of the excel before editing
        del originalFrame[originalFrame.columns[0]]
        list_data = originalFrame.values.tolist()
        print("Excel file Exists")

        ls  = list(originalFrame.columns)                                   #current iteration number  
        print(ls[len(ls)-1])
        numList= re.findall(r'\d+',ls[len(ls)-1])
        print(numList)
        number=int(float(''.join(numList)))
        print(number)
        newNum=number+1

        currentData = pd.DataFrame({ f'Index {newNum}': dataA, f'Pinky {newNum}': dataB,
                                  f'Thumb {newNum}': dataC})
        
        newDataFrame = pd.concat([originalFrame, currentData], axis=1)      #add current data to old data

        timeIndex=[]

        #creating the Time collumn
        if originalFrame.shape[0] < currentData.shape[0]:                   #if new data is longer
            print("its bigger")
            for i in range(len(dataA)):
                timeIndex.append(float(i)/100)
        else:                                                               #If origonal data is longer
            print("its not")
            for i in range(originalFrame.shape[0]-1):
                timeIndex.append(float(i)/100)

        timeFrame=pd.DataFrame({ "Time":timeIndex})                         
        wholeFrame=pd.concat([timeFrame, newDataFrame], axis=1)             #adding time to the new data

        wholeFrame.to_excel('data.xlsx', index=False, engine='openpyxl')    #Writing the whole date to excel
        print("writing")
        print(wholeFrame)
        #write_to_excel(df)
        print(wholeFrame.shape[0])
    except FileNotFoundError:               # If the file doesn't exist, create a new dataframe
        print("file does not exist, creating file")
        timeIndex=[]
        for i in range(len(dataA)):         #time array to match the frame
            timeIndex.append(float(i)/100)
        print(timeIndex)    
        currentData = pd.DataFrame({ "Time":timeIndex,f'Index 1': dataA, f'Pinky 1': dataB,   #Write the current data
                                  f'Thumb 1': dataC})
        currentData.to_excel('data.xlsx', index=False, engine='openpyxl')
        print("writing")
        print(currentData)
############################################################################################################
write_to_excel(indexList,pinkyList,thumbList)           #Calls the function above

