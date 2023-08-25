import math


"""

pinkyCoord  =   [8, 1]        #Pinky cooridnate is point of refferance
indexCoord  =   [pinkyCoord[0], pinkyCoord[1] + 4.5]
thumbCoord  =   [pinkyCoord[0] -6.622, pinkyCoord[1] +1.93]

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


thumbToPinky = 6.9
thumbToIndex = 7.1
indexToPinky = 4.5

pinkyCoord  =   [8, 1]        #Pinky cooridnate is point of refferance
indexCoord  =   [pinkyCoord[0], pinkyCoord[1] + 4.5]
thumbCoord  =   [pinkyCoord[0] -6.622, pinkyCoord[1] +1.93]


print("OrigonalList is "+str( pinkyCoord   )+str( indexCoord   )+str( thumbCoord   )+" \n")

thing1,thing2,thing3 = returnCoordinates(thumbToPinky, thumbToIndex,indexToPinky )
print(thing1[0])
print(   "Calculated" + str(returnCoordinates(thumbToPinky, thumbToIndex,indexToPinky )))

