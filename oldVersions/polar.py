
import math
import numpy as np

x = 1
y = -1

#90 degrees is 1.57 radians

r=math.sqrt(x**2 + y**2)

if(x>0):
    theta = (np.arctan(y/x))   
else:
    theta = (np.arctan(y/x))+np.pi

if(theta<0):
    theta = (2*np.pi)+theta


thetaDegrees = theta *  (180/np.pi)
print("X is "+str(x))
print("Y is "+str(y))


print("\nR is "+str(r) )


print("Theta radians "+ str(theta ) )
print("Theta degrees "+ str( thetaDegrees  ))


print("\n\n After the change")
correctedAmount= thetaDegrees-(thetaDegrees-90)



numSteps = -(thetaDegrees-90)
print("corrected Amount is "+str(correctedAmount))
print("Num steps is "+ str(numSteps) )


if 90 < thetaDegrees <= 270:
    print("Clockwise : " + str((thetaDegrees-90) ))
else:
    if(thetaDegrees <90):
        print("Counter Clockwise : " + str(90 -thetaDegrees ))
    else:    
        print("Counter Clockwise : " + str(  90+(360-thetaDegrees) ))