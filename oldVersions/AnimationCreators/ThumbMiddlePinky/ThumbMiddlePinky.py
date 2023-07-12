import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as image
import pandas as pd
import time
import os.path


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

def getIterationArray(iterationIndex):              #returns a 2D array with Thumb, Middle and Pinky Data
    temp = ''
    increaseIndex = 3       #index that the values start at
    thumbArr = []               #Empty arrays
    middleArr = []
    pinkyArr = []

    while pd.isnull(temp) == False:             #While the value in the Excel collumn is not Nan, reads from top to bottom
        temp = list_data[increaseIndex][iterationIndex]         #Thumb collum
        temp2 = list_data[increaseIndex][iterationIndex+1]      #middle collum
        temp3 = list_data[increaseIndex][iterationIndex+2]      #pinky collum

        thumbArr.append(temp)               #append each Thumb value to the indexArray list
        middleArr.append(temp2)              #append each Middle value to the pinkyArray list
        pinkyArr.append(temp3)              #append each Pinky value to the thumbArray list
        increaseIndex += 1      #index to iterate over every row

    threeDataPoints = []             #Individual iteration consisting of values from all 3 fingers
    threeDataPoints.append(thumbArr)
    threeDataPoints.append(middleArr)
    threeDataPoints.append(pinkyArr)

    return(threeDataPoints)

def getCogCoordniates():
    global TwoDArray
    global thumbCoord
    global middleCoord
    global pinkyCoord

    for i in range(len(TwoDArray[1])):         #for loop, runs the length of the list
        force = [float(TwoDArray[0][i]), float(TwoDArray[1][i]), float(TwoDArray[2][i])] #3 force values for each finger
        if (force[0] + force[1] + force[2]) == 0:                      #If forces are all 0
            xPoint = 0                              #Set coordinates to 0, cannot divide by 0
            yPoint = 0
        else:                                       #else, Calculate center of gravity
            xPoint = (thumbCoord[0] * force[0] + middleCoord[0] * force[1] + pinkyCoord[0] * force[2]) / (force[0] + force[1] + force[2])
            yPoint = (thumbCoord[1] * force[0] + middleCoord[1] * force[1] +  pinkyCoord[1] * force[2]) / (force[0] + force[1] + force[2])
###############################Flag above


        cogCoordinates.append((xPoint, yPoint))          #append each Cog to a list 
    return cogCoordinates

def create_folder(folder_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    new_folder_path = os.path.join(current_dir, folder_name)
    
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")
#######################################################################################################################
SaveIndex = 1



filePath = 'newest.xlsx'                   # this is the file path of the Excel sheet
sheet = 6                                     # Usually 2


if(os.path.exists(filePath)):
    print("The file path Exists")
    df = pd.read_excel(filePath, sheet_name = sheet)
    list_data = df.values.tolist()
    xl = pd.ExcelFile(filePath)

      # see all sheet names
    print("Working with sheet"+ xl.sheet_names[2])
    folderName=xl.sheet_names[sheet]

    #folder_name = folderName

    # Call the function to create the folder
    create_folder(folderName)
    for i in  range( len(list_data[0]) -1):

        iterationIndex = 1+(4*i)          #Do in increments of 4

        saveName = f"{folderName}/Animation"

        saveName=saveName+str(i+1)+".mp4"
        print("Creating "+ saveName)
        TwoDArray=getIterationArray(iterationIndex)     #contains 3 data points

        pinkyCoord = [10, 1]        #Pinky cooridnate is point of refferance
        middleCoord = [pinkyCoord[0], pinkyCoord[1] + 10]
        thumbCoord = [pinkyCoord[0] - 8.485, pinkyCoord[1] + 7]

        """ CogX= ( (x1*f1) + (x2*f2) + (x3*f3) ) / (f1+f2+f3)
            CogY= ( (y1*f1) + (y2*f2) + (y3*f3) ) / (f1+f2+f3)"""
        cogCoordinates=[]
        cogCoordinates=getCogCoordniates()



        #######################################################################################################################
        fig, ax = plt.subplots()            # Settings for the graph
        plt.grid()
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 12)

        iterationNumber = list_data[1][iterationIndex]
        iterationLabel =ax.text(2,12.2, f"Iteration: {iterationNumber}" , ha='center', va='bottom')

        print("Iteration " + str( iterationNumber ))

            #Exact points of each sensor. These are fixed
        pinky_point, = ax.plot(pinkyCoord[0], pinkyCoord[1], 'ro')      
        pinky_label = ax.text(pinkyCoord[0], pinkyCoord[1] - 1, 'Pinky', ha='center', va='bottom')

        middle_point, = ax.plot(middleCoord[0], middleCoord[1], 'bo')
        middle_label = ax.text(middleCoord[0], middleCoord[1] - 1, 'Middle', ha='center', va='bottom')

        thumb_point, = ax.plot(thumbCoord[0], thumbCoord[1], 'go')
        thumb_label = ax.text(thumbCoord[0], thumbCoord[1] - 1, 'Thumb', ha='center', va='bottom')

        Cog_point, = ax.plot([], [], 'yo')           #COG point moves
        Cog_label = ax.text([], [], 'Center of gravity', ha='center', va='bottom')

        timeLabel = ax.text(5, 12.2, 'Time: ')        #Displays the time

        imagePath = ["pinkyFinger.png","middleFinger.png","thumbFinger.png"]     #paths of the icons for the images
        logo = image.imread(imagePath[0])
        image_position = [pinkyCoord[0]-0.42, pinkyCoord[1]-0.27]  # Position of the image
        ax.imshow(logo, extent=[image_position[0], image_position[0] + 1, image_position[1], image_position[1] + 1])

        middleLogo=image.imread(imagePath[1])
        middleLogoPos = [middleCoord[0], middleCoord[1]+0.3]  # Position of the image
        ax.imshow(middleLogo, extent=[middleLogoPos[0]-0.5, middleLogoPos[0] + 0.5, middleLogoPos[1]-0.5, middleLogoPos[1] + 0.5])

        thumbLogo=image.imread(imagePath[2])
        thumbLogoPos = [thumbCoord[0]-0.5, thumbCoord[1] - 0.5]  # Position of the image
        ax.imshow(thumbLogo, extent=[thumbLogoPos[0], thumbLogoPos[0] + 1, thumbLogoPos[1], thumbLogoPos[1] + 1])
        #####################################################################################################################



        lines = []
        threshold = getThresholdValue(TwoDArray[0])
        for i in range(len(cogCoordinates) - 1):                     #for i in range of the list
            x_coords = [cogCoordinates[i][0], cogCoordinates[i + 1][0]]       #The coordinates of the line to be plotted 
            y_coords = [cogCoordinates[i][1], cogCoordinates[i + 1][1]]

            color = 'green'                                     #default color

            if TwoDArray[0][i]<threshold:                      #Colors for each line
                color = 'red'
            else:   #Ending
                color = 'green'

            if color=="red" and i> len(cogCoordinates)/4:       #if color below threshold and after first quarter
                color = 'blue'

            line, = ax.plot(x_coords, y_coords, color=color, alpha=0)   #Trajectory path the COG will move over next
            lines.append(line)

        ##The graph plots the entire path of the Cog, but most of it is invisible until the alpha value is set greater than 0
        def update(frame):
            x, y = cogCoordinates[frame]
            
            Cog_point.set_data([x], [y])
            Cog_label.set_text(f'Center of gravity: ({round(x, 1)}, {round(y, 1)})')
            Cog_label.set_position((x, y + 0.5))

            timeLabel.set_text(f'Time: {frame}')

            if frame < len(lines):
                lines[frame].set_alpha(1.0)             #sets current path line to darkest color
                lines[frame - 1].set_alpha(0.2)         #sets previous line to light color   
                if frame < len(lines) - 5:              # 5 from the end    
                    lines[frame + 1].set_alpha(0.8)     #displaying the next 5 lines   
                    lines[frame + 2].set_alpha(0.8)
                    lines[frame + 3].set_alpha(0.8)
                    lines[frame + 4].set_alpha(0.8)
                    lines[frame + 5].set_alpha(0.8)

            if frame < 10 or   frame > len(lines)-7  : #slows down the sketch at the bbeginning and end of the process
                time.sleep(5)    

        #calls the update function
        ani = animation.FuncAnimation(fig, update, frames=len(lines) + 1, interval=120, repeat=False)       
        ani.save(saveName, writer='ffmpeg')

        #plt.show()

        print("Theshold value "+str(getThresholdValue(TwoDArray[0])))

else:
    print(f"The file path {filePath} does not exist")    
    exit()


print("Program has Ended")
