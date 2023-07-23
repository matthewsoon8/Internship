


"""
Version 4
First fully working version
Notes: This recieves 4 values from the arduino+
        Thumb pressure
        Pinky pressure
        Index pressure
        the angle the arduino wants to correct
    Must have FFmpeg installed


"""
#Libraries needed
import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as image
import serial
import serial.tools.list_ports
import pandas as pd
import re


"""
Record the distances between the fingers, then replace these values
"""
thumbToPinky    = 8.7
thumbToIndex    = 7
indexToPinky    = 5.2

#Its best to  have them both on or both off
writeToExcel    = 1             #If this is 1, the program will Write to an excel file    
yesAnimate      = 1             #If this is 1, the program will output an animation

autoDetectDevice = 1

#USB Serial Port        USB-SERIAL
stringName = "USB Serial Port"

"""
Returns coordinates of a 3 finger system given the distances between 3 fingers
"""
def returnCoordinates(thumbToPinky, thumbToIndex,indexToPinky):
    sideB = indexToPinky
    sideA = thumbToIndex    #A
    sideC = thumbToPinky

    pinkyAngle = math.degrees(math.acos( ((sideC**2 + sideB**2) - sideA**2) / (2 * sideC * sideB)  ))
    indexAngle = math.degrees(math.acos( ((sideA**2 + sideB**2) - sideC**2) / (2 * sideA * sideB)  ))
    thumbAngle = 180-pinkyAngle - indexAngle
    #print("Whole Triangle. Angle 1 is " + str(pinkyAngle) + " , Angle 2 is " +str(indexAngle) +" ,Angle 3 is " +str(thumbAngle)+"\n")

    topTriangle = 180-90-indexAngle
    #print("Top Triangle Angle 1: "+str(topTriangle) + " , Angle2: "+str(angle2)+ " , Angle3: "+str(90))

    longLength = math.sin(math.radians(indexAngle)) * thumbToIndex
    #print("Height is "+ str(longLength))

    bottomTriangle = 180-90-pinkyAngle
    #print("Top Triangle Angle 1: "+str(bottomTriangle) + " , Angle2: "+str(angle1)+ " , Angle3: "+str(90))
    bottomTriangleLength = math.cos(math.radians(pinkyAngle))*thumbToPinky

    pinkyCoordinate = (math.ceil(longLength+1) ,   1 )
    indexCoord  =   (round(pinkyCoordinate[0],2) , round(pinkyCoordinate[1] + indexToPinky,2))
    thumbCoord  =   (round(pinkyCoordinate[0] -longLength,2)   ,    round(pinkyCoordinate[1] + bottomTriangleLength,2))
    
    return (pinkyCoordinate, indexCoord,thumbCoord)


pinkyCoord,indexCoord,thumbCoord = returnCoordinates(thumbToPinky, thumbToIndex,indexToPinky )
print(str(returnCoordinates(thumbToPinky, thumbToIndex,indexToPinky )))
graphLimitX= (0,math.ceil(pinkyCoord[0] +1))
graphLimitY= (0,math.ceil(indexCoord[1] +1))

indexList=[]
thumbList=[]
pinkyList=[]
angleList=[]

timeArray=0
indexNum=0

COPcoordinates=[]
dataList = []                                           # Create empty list variable for later use

fig, ax = plt.subplots()            # Settings for the graph
plt.grid()
ax.set_xlim(graphLimitX[0], graphLimitX[1])
ax.set_ylim(graphLimitY[0], graphLimitY[1])
timeLabel = ax.text(4, 7.2, 'Time: ') 
pinky_point, = ax.plot(pinkyCoord[0], pinkyCoord[1], 'ro')      
pinky_label = ax.text(pinkyCoord[0], pinkyCoord[1] - 1, 'Pinky', ha='center', va='bottom')
index_point, = ax.plot(indexCoord[0], indexCoord[1], 'bo')
index_label = ax.text(indexCoord[0], indexCoord[1] - 1, 'Index', ha='center', va='bottom')
thumb_point, = ax.plot(thumbCoord[0], thumbCoord[1], 'go')
thumb_label = ax.text(thumbCoord[0], thumbCoord[1] - 1, 'Thumb', ha='center', va='bottom')

xPoint1 = (indexCoord[0] + pinkyCoord[0] + thumbCoord[0] ) / 3
yPoint2 = (indexCoord[1] + pinkyCoord[1] + thumbCoord[1] ) / 3

trueCenter, = ax.plot(xPoint1, yPoint2, 'ko')
trueCenterLabel = ax.text(xPoint1, yPoint2- 1, 'Center', ha='center', va='bottom')

Cog_point, = ax.plot([], [], 'mP', markersize=20)           #COG point moves
Cog_label = ax.text(1, 1, 'Center of Preasure', ha='center', va='bottom')
imagePath = ["pinkyFinger.png","indexFinger.png","thumbFinger.png"]     #paths of the icons for the images
logo = image.imread(imagePath[0])
image_position = [pinkyCoord[0]-0.42, pinkyCoord[1]-0.27]  # Position of the image
ax.imshow(logo, extent=[image_position[0], image_position[0] + 1, image_position[1], image_position[1] + 1])
indexLogo=image.imread(imagePath[1])
indexLogoPos = [indexCoord[0], indexCoord[1]+0.3]  # Position of the image
ax.imshow(indexLogo, extent=[indexLogoPos[0]-0.5, indexLogoPos[0] + 0.5, indexLogoPos[1]-0.5, indexLogoPos[1] + 0.5])
thumbLogo=image.imread(imagePath[2])
thumbLogoPos = [thumbCoord[0]-0.5, thumbCoord[1] - 0.5]  # Position of the image
ax.imshow(thumbLogo, extent=[thumbLogoPos[0], thumbLogoPos[0] + 1, thumbLogoPos[1], thumbLogoPos[1] + 1])


"""
Purpose: This function is the main loop of the program. 
Notes:  This is the function that is actually called at the end of the program
"""
################################################################################################################
##########################################   Main    ###########################################################
def main():                                                        
    global fig,ax
    global pinkyCoord 
    global indexCoord 
    global thumbCoord 
    global COPcoordinates
    global indexNum

    comPort=gerArduinoComPort()
    print(comPort)

    ser = serial.Serial(comPort, 115200)                       # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
    #ser = serial.Serial("COM5", 9600)                       
    time.sleep(2)                                           # Time delay for Arduino Serial initialization 

    ani = animation.FuncAnimation(fig, liveAnimation, frames=100, fargs=(pinkyList, ser), interval=100) 
    #ani.save("stringName.mp4", writer='ffmpeg')

    plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed
    ser.close()                                             # Close Serial connection when plot is closed

    if writeToExcel==1:
        write_to_excel(indexList,pinkyList,thumbList, angleList)           #Calls the function above



    #####################################################             Post Processing, Animation MP4          ##################################################
    ############################################################################################################################################################
    """
    Purpose: This part of the main function gives the user the oportunity to save an animation
    Notes:  This animation is created if Yes animate is 1. if it is 0, nothing is done
            This animation is created after the current program runs during post processing
    """

    global yesAnimate
    
    if(yesAnimate==1):
        fig, ax = plt.subplots()            # Settings for the graph
        plt.grid()
        ax.set_xlim(graphLimitX[0], graphLimitX[1])
        ax.set_ylim(graphLimitY[0], graphLimitY[1])

        global timeLabel
        global pinky_point
        global pinky_label
        global index_point
        global index_label
        global thumb_point
        global thumb_label
        global trueCenter
        global trueCenterLabel
        global Cog_point
        global Cog_label

        timeLabel = ax.text(4, 7.2, 'Time: ') 
        pinky_point, = ax.plot(pinkyCoord[0], pinkyCoord[1], 'ro')      
        pinky_label = ax.text(pinkyCoord[0], pinkyCoord[1] - 1, 'Pinky', ha='center', va='bottom')
        index_point, = ax.plot(indexCoord[0], indexCoord[1], 'bo')
        index_label = ax.text(indexCoord[0], indexCoord[1] - 1, 'Index', ha='center', va='bottom')
        thumb_point, = ax.plot(thumbCoord[0], thumbCoord[1], 'go')
        thumb_label = ax.text(thumbCoord[0], thumbCoord[1] - 1, 'Thumb', ha='center', va='bottom')

        xPoint1 = (indexCoord[0] + pinkyCoord[0] + thumbCoord[0] ) / 3
        yPoint2 = (indexCoord[1] + pinkyCoord[1] + thumbCoord[1] ) / 3

        trueCenter, = ax.plot(xPoint1, yPoint2, 'ko')
        trueCenterLabel = ax.text(xPoint1, yPoint2- 1, 'Center', ha='center', va='bottom')

        Cog_point, = ax.plot([], [], 'mP', markersize=20)           #COG point moves
        Cog_label = ax.text(1, 1, 'Center of Preasure', ha='center', va='bottom')
        imagePath = ["pinkyFinger.png","indexFinger.png","thumbFinger.png"]     #paths of the icons for the images
        logo = image.imread(imagePath[0])
        image_position = [pinkyCoord[0]-0.42, pinkyCoord[1]-0.27]  # Position of the image
        ax.imshow(logo, extent=[image_position[0], image_position[0] + 1, image_position[1], image_position[1] + 1])
        indexLogo=image.imread(imagePath[1])
        indexLogoPos = [indexCoord[0], indexCoord[1]+0.3]  # Position of the image
        ax.imshow(indexLogo, extent=[indexLogoPos[0]-0.5, indexLogoPos[0] + 0.5, indexLogoPos[1]-0.5, indexLogoPos[1] + 0.5])
        thumbLogo=image.imread(imagePath[2])
        thumbLogoPos = [thumbCoord[0]-0.5, thumbCoord[1] - 0.5]  # Position of the image
        ax.imshow(thumbLogo, extent=[thumbLogoPos[0], thumbLogoPos[0] + 1, thumbLogoPos[1], thumbLogoPos[1] + 1])

        print("Performing post processing")
        print("Number of frames "+str(len(COPcoordinates)))
        ani = animation.FuncAnimation(fig, postAnimation, frames=len(COPcoordinates) , interval=100, repeat=False)       
        stringName = f"{indexNum}Video.mp4"
        ani.save(stringName, writer='ffmpeg')


    print("Program Complete")



#########################################################################################################################################################
#########################################################################################################################################################
###################################################                 FunctionsBelow                 ######################################################
#########################################################################################################################################################
#########################################################################################################################################################


################################                Animation Functions             ###########################################
"""
Purpose: This function is the live animation that is displayed when the program runs.
Notes:  This animation is a delayed live animation
"""
def liveAnimation(i, pinkyList, ser):
    global indexList
    global thumbList
    global timeArray
    global angleList

    ser.write(b'g')                                     # Transmit the char 'g' to the Arduino so it knows to send data
    arduinoData_string = ser.readline().decode('ascii') # recieved value from the arduino
    
    splitData=arduinoData_string.split(",")                 #Split data oncommas [index],[Thumb],[Pinky], Angle
    
    print(float(splitData[2]))

    try:                                            #individually add each datapoint to the list
        arduinoVal1 = float(splitData[0])                   # Convert to float
        indexList.append(arduinoVal1)               # add each point to its corrosponding list
        arduinoVal2= float(splitData[1])
        pinkyList.append(arduinoVal2)
        arduinoVal3= float(splitData[2])
        thumbList.append(arduinoVal3)
        arduinoVal4= float(splitData[3])
        angleList.append(arduinoVal4)

    except:                                             # Pass if data point is bad                               
        pass

    if arduinoVal1 + arduinoVal2 + arduinoVal3==0:      #If all pressure values are 0, move the COP off the map
        xPoint=20
        yPoint=20
    else:                
        xPoint = (indexCoord[0] * arduinoVal1 + pinkyCoord[0] * arduinoVal2 + thumbCoord[0] * arduinoVal3) / (arduinoVal1 + arduinoVal2 + arduinoVal3)
        yPoint = (indexCoord[1] * arduinoVal1 + pinkyCoord[1] * arduinoVal2 +  thumbCoord[1] * arduinoVal3) / (arduinoVal1 + arduinoVal2 + arduinoVal3)
    
    COPcoordinates.append((xPoint,yPoint))

    Cog_point.set_data(xPoint, yPoint)
    #Cog_label.set_text(f'Center of gravity: ({round(xPoint, 1)}, {round(yPoint, 1)})')
    Cog_label.set_position((xPoint, yPoint + 0.5))
    timeLabel.set_text(f'Time: {timeArray}')
    timeArray +=1


"""
Purpose: This function creates an animation that is sent back to the main loop.
Notes:  This animation is created after the program closes and takes a while to run
"""
def postAnimation(frame):
    global COPcoordinates               #Global labels
    global Cog_point
    global Cog_label
    global timeLabel
    x, y = COPcoordinates[frame]
    
    Cog_point.set_data([x], [y])        #Animation
    Cog_label.set_text(f'Center of Preasure: ({round(x, 1)}, {round(y, 1)})')
    Cog_label.set_position((x, y + 0.5))

    timeLabel.set_text(f'Time: {frame}')

    if frame < 10 or   frame > len(COPcoordinates)-7  : #slows down the sketch at the bbeginning and end of the process
        time.sleep(5)    


"""
Purpose: This function returns the com port number that the arduino is on.
"""
def gerArduinoComPort():
    global stringName                                   #name of device specified at the top
    portNum = None
    ports = list( serial.tools.list_ports.comports())    #gets list of ports
           
    for i in  range(len(ports)):                    #loops through all the port numbers
        currentObject = str(ports[i])               #object of the current port iteration

        if stringName in currentObject:             #if device name is in the object we are currently looking at
            print("Device Found")               
            print(currentObject)
            newstr = currentObject.split(" - ")          #Serapates the port number and the device name
            portNum=newstr[0]
        else:
            print("Devices Com port not Found")    

    return(portNum)                                 #Port number that the device is found on


"""
Purpose: This function Writes the test data to an excel file
Notes: The excel file will be created if there is not one in the directory
Data A is 
Data B is 
Data C is 
Data D is Angle of COP calculated by the arduino
"""
def write_to_excel(dataA, dataB, dataC, dataD):
    global indexNum
    try:                        # Try to read the existing file
        originalFrame = pd.read_excel('data.xlsx', engine='openpyxl')               #reads contents of the excel before editing
        del originalFrame[originalFrame.columns[0]]                                 #Remove first collum(time collum) for easier usage
        list_data = originalFrame.values.tolist()                                   #Convert to a list
        print("Excel file already Exists")                                          #prints if the above worked

        ls  = list(originalFrame.columns)                                           #current iteration number  
        print(ls[len(ls)-1])                                                        #prints the last object written to the excel sheet
        numList= re.findall(r'\d+',ls[len(ls)-1])                                   #Finds all numbers
        print(numList)                                                              #prints the iteration number of the previous value
        number=int(float(''.join(numList)))                                 
        print(number)                                                               #prints the iteration number of the previous value
        newNum=number+1                                                             #current test number will be 1 more than last one in the excel
        indexNum = newNum
        currentData = pd.DataFrame({ f'Index {newNum}': dataA, f'Pinky {newNum}': dataB,            #Creating a current dataframe of current test data
                                  f'Thumb {newNum}': dataC, f'COPAngle {newNum}': dataD})
        
        newDataFrame = pd.concat([originalFrame, currentData], axis=1)              #add current data to old data

        timeIndex=[]

        #creating the Time collumn
        if originalFrame.shape[0] < currentData.shape[0]:                           #if new data is longer
            print("New data has more time points than previous")
            for i in range(len(dataA)):
                timeIndex.append(float(i)/100)
        else:                                                                       #If origonal data is longer
            print("new data las less time points than the previous")
            for i in range(originalFrame.shape[0]-1):
                timeIndex.append(float(i)/100)

        timeFrame=pd.DataFrame({ "Time":timeIndex})                         
        wholeFrame=pd.concat([timeFrame, newDataFrame], axis=1)                     #adding time to the new data

        wholeFrame.to_excel('data.xlsx', index=False, engine='openpyxl')            #Writing the whole date to excel
        print("writing")
        print(wholeFrame)
        print(wholeFrame.shape[0])
    except FileNotFoundError:                                                       # If the file doesn't exist, create a new dataframe
        print("file does not exist, creating file")
        timeIndex=[]
        indexNum=1
        for i in range(len(dataA)):                                                 #time array to match the frame
            timeIndex.append(float(i)/100)
        print(timeIndex)    
        currentData = pd.DataFrame({ "Time":timeIndex,f'Index 1': dataA, f'Pinky 1': dataB,   #Write the current data
                                  f'Thumb 1': dataC, f'COPAngle 1': dataD})
        currentData.to_excel('data.xlsx', index=False, engine='openpyxl')
        print("writing")
        print(currentData)
########################################################################################################################################################


"""
Purpose:This is where the main loop is called
Notes:  This allows most functions to be placed below the main loop function because
        the main loop is actually called at the very end of the program
"""
if __name__ == "__main__":
    main()