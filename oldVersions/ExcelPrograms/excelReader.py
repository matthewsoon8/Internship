import pandas as pd
import re

def write_to_excel(dataA,dataB,dataC):

    try:                        # Try to read the existing file
        df = pd.read_excel('data.xlsx', engine='openpyxl')
        del df[df.columns[0]]
        list_data = df.values.tolist()
        print("file Exists")

        ls  = list(df.columns)
        print(ls[len(ls)-1])
        numList= re.findall(r'\d+',ls[len(ls)-1])
        print(numList)
        number=int(float(''.join(numList)))
        print(number)
        newNum=number+1

        dataFrame2 = pd.DataFrame({ f'Index {newNum}': dataA, f'Pinky {newNum}': dataB,
                                  f'Thumb {newNum}': dataC})
        newDataFrame = pd.concat([df, dataFrame2], axis=1) 


        timeIndex=[]
        for i in range(len(dataA)):
            timeIndex.append(i)

        dataFrame3=pd.DataFrame({ "Time":timeIndex})
        third=pd.concat([dataFrame3, newDataFrame], axis=1) 

        third.to_excel('data.xlsx', index=False, engine='openpyxl')
        print("writing")
        print(third)
        #write_to_excel(df)

    except FileNotFoundError:           # If the file doesn't exist, create a new dataframe
        print("file does not exist")
        timeIndex=[]
        for i in range(len(dataA)):
            timeIndex.append(i)
        print(timeIndex)    
        df = pd.DataFrame({ "Time":timeIndex,f'Index 1': dataA, f'Pinky 1': dataB,
                                  f'Thumb 1': dataC})
        df.to_excel('data.xlsx', index=False, engine='openpyxl')
        print("writing")
        print(df)

# Test data
dataA = [1,2,3,4,5]

# Call the function
write_to_excel(dataA,dataA,dataA)
