import time
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as image
import serial
import serial.tools.list_ports
import pandas as pd
import re



thumbToPinky    = 6.9
thumbToIndex    = 7.1
indexToPinky    = 4.5

yesAnimate      = 0          #If this is 1, the program will output an animation
writeToExcel    = 0             #If this is 1, the program will Write to an excel file    

autoDetectDevice= 1

#USB Serial Port        USB-SERIAL
stringName = "USB Serial Port"




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
graphLimitX= (0,math.ceil(pinkyCoord[0] +1))
graphLimitY= (0,math.ceil(indexCoord[1] +1))

"""ax.set_xlim(0, 9)
ax.set_ylim(0, 7)"""




indexList=[]
thumbList=[]
pinkyList=[]
timeArray=0
indexNum=0
cogCoordinates=[]
dataList = []                                           # Create empty list variable for later use
lines = []

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

def main():                                                        
    global fig,ax
    global pinkyCoord 
    global indexCoord 
    global thumbCoord 

    comPort=gerArduinoComPort()
    print(comPort)

    ser = serial.Serial(comPort, 9600)                       # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
    #ser = serial.Serial("COM5", 9600)                       
    time.sleep(2)                                           # Time delay for Arduino Serial initialization 

    ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(pinkyList, ser), interval=100) 

    #ani.save("stringName.mp4", writer='ffmpeg')

    plt.show()                                              # Keep Matplotlib plot persistent on screen until it is closed
    ser.close()                                             # Close Serial connection when plot is closed

    if writeToExcel==1:
        write_to_excel(indexList,pinkyList,thumbList)           #Calls the function above



    #####################################################             Post Processing, Animation MP4          ##################################################
    ############################################################################################################################################################
    ############################################################################################################################################################
    ############################################################################################################################################################
    ############################################################################################################################################################
    global yesAnimate

    if(yesAnimate==1):
        fig, ax = plt.subplots()            # Settings for the graph
        plt.grid()
        ax.set_xlim(graphLimitX[0], graphLimitX[1])
        ax.set_ylim(graphLimitY[0], graphLimitY[1])


        #iterationLabel =ax.text(2,12.2, f"Iteration: " , ha='center', va='bottom')

        #########################           Finger point settings             #######################################################
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


        global lines
        threshold = getThresholdValue(indexList)
        for i in range(len(cogCoordinates) - 1):                                #Getting the Lines
            x_coords = [cogCoordinates[i][0], cogCoordinates[i + 1][0]]       #The coordinates of the line to be plotted 
            y_coords = [cogCoordinates[i][1], cogCoordinates[i + 1][1]]

            color = 'green'                                     #default color

            if indexList[i]<threshold:                      #Colors for each line
                color = 'red'
            else:   #Ending
                color = 'green'

            if color=="red" and i> len(cogCoordinates)/4:       #if color below threshold and after first quarter
                color = 'blue'

            line, = ax.plot(x_coords, y_coords, color=color, alpha=0)   #Trajectory path the COG will move over next
            lines.append(line)

        print("\n\n")
        lines = []
        print(cogCoordinates)
        print("\n\n")

        print(cogCoordinates[0][0])

        for i in range(len(cogCoordinates) - 1):                     #for i in range of the list
            x_coords = [cogCoordinates[i][0], cogCoordinates[i + 1][0]]       #The coordinates of the line to be plotted 
            y_coords = [cogCoordinates[i][1], cogCoordinates[i + 1][1]]

            color = 'green'                                     #default color
            """
            if indexList[i]<threshold:                      #Colors for each line
                color = 'red'
            else:   #Ending
                color = 'green'

            if color=="red" and i> len(cogCoordinates)/4:       #if color below threshold and after first quarter
                color = 'blue'
            
            line, = ax.plot(x_coords, y_coords, color=color, alpha=0)   #Trajectory path the COG will move over next
            """
            lines.append(line)
        

        #calls the update function

        print("Number of frames: "+str(len(lines)))
        print("Performing post processing")
        ani = animation.FuncAnimation(fig, animationFunction2, frames=len(lines) + 1, interval=100, repeat=False)       

        stringName = f"{indexNum}Video.mp4"
        ani.save(stringName, writer='ffmpeg')


    print("Finished running")






#########################################################################################################################################################
#########################################################################################################################################################
###################################################                 FunctionsBelow                 ######################################################
#########################################################################################################################################################
#########################################################################################################################################################


def getThresholdValue( numList ):
    total=0
    length=0
    for i in range (len(numList)):
        if numList[i] !="Index" and pd.isnull(numList[i]) ==False :
            if float(numList[i]) > -1:
                #numbsList.append(float(numList[i]) )
                total=total+float(numList[i])
                length=length+1

    avg=total/length
    return(round(avg,2))

################################                Animation stuff             ###########################################

def animate(i, pinkyList, ser):
    global indexList
    global thumbList
    global timeArray

    ser.write(b'g')                                     # Transmit the char 'g' to the Arduino so it knows to send data
    arduinoData_string = ser.readline().decode('ascii') # recieved value from the arduino
    
    splitData=arduinoData_string.split(",")                 #Split data oncommas [index],[Thumb],[Pinky]
    
    val1 = splitData[0]
    val2 = splitData[1]
    val3 = splitData[2]

    print(float(splitData[2]))

    try:         #individually add each datapoint to the list
        arduinoVal1 = float(val1)                   # Convert to float
        indexList.append(arduinoVal1)              # add each point to its corrosponding list
        arduinoVal2= float(val2)
        pinkyList.append(arduinoVal2)
        arduinoVal3= float(val3)
        thumbList.append(arduinoVal3)

    except:                                             # Pass if data point is bad                               
        pass

    if arduinoVal1 + arduinoVal2 + arduinoVal3==0:
        xPoint=20
        yPoint=20
    else:                
        xPoint = (indexCoord[0] * arduinoVal1 + pinkyCoord[0] * arduinoVal2 + thumbCoord[0] * arduinoVal3) / (arduinoVal1 + arduinoVal2 + arduinoVal3)
        yPoint = (indexCoord[1] * arduinoVal1 + pinkyCoord[1] * arduinoVal2 +  thumbCoord[1] * arduinoVal3) / (arduinoVal1 + arduinoVal2 + arduinoVal3)
    
    cogCoordinates.append((xPoint,yPoint))

    Cog_point.set_data(xPoint, yPoint)
    #Cog_label.set_text(f'Center of gravity: ({round(xPoint, 1)}, {round(yPoint, 1)})')
    Cog_label.set_position((xPoint, yPoint + 0.5))
    timeLabel.set_text(f'Time: {timeArray}')
    timeArray +=1


def write_to_excel(dataA, dataB, dataC):
    global indexNum
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
        indexNum = newNum
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
        indexNum=1
        for i in range(len(dataA)):         #time array to match the frame
            timeIndex.append(float(i)/100)
        print(timeIndex)    
        currentData = pd.DataFrame({ "Time":timeIndex,f'Index 1': dataA, f'Pinky 1': dataB,   #Write the current data
                                  f'Thumb 1': dataC})
        currentData.to_excel('data.xlsx', index=False, engine='openpyxl')
        print("writing")
        print(currentData)
############################################################################################################

def animationFunction2(frame):
    x, y = cogCoordinates[frame]
    
    Cog_point.set_data([x], [y])
    Cog_label.set_text(f'Center of Preasure: ({round(x, 1)}, {round(y, 1)})')
    Cog_label.set_position((x, y + 0.5))

    timeLabel.set_text(f'Time: {frame}')
    """
    if frame < len(lines):
        lines[frame].set_alpha(1.0)             #sets current path line to darkest color
        lines[frame - 1].set_alpha(0.2)         #sets previous line to light color   
        if frame < len(lines) - 5:              # 5 from the end    
            lines[frame + 1].set_alpha(0.8)     #displaying the next 5 lines   
            lines[frame + 2].set_alpha(0.8)
            lines[frame + 3].set_alpha(0.8)
            lines[frame + 4].set_alpha(0.8)
            lines[frame + 5].set_alpha(0.8)
    """
    if frame < 10 or   frame > len(lines)-7  : #slows down the sketch at the bbeginning and end of the process
        time.sleep(5)    

def gerArduinoComPort():
    global stringName
    portNum= None
    ports =list( serial.tools.list_ports.comports())
           
    strThing=str(ports[0])
    print(ports[0])

    for i in  range(len(ports)):
        currentObject = str(ports[i])

        if stringName in currentObject:
            print("Device Found")
            newstr = strThing.split(" - ")
            portNum=newstr[0]
        else:
            print("Devices Com port not Found")    

    return(portNum)

if __name__ == "__main__":
    main()