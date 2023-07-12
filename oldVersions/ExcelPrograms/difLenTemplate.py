"""
This program appends a larger collum to a smaller collum in pandas

https://stackoverflow.com/questions/27126511/add-columns-different-length-pandas

"""


# importing pandas
import pandas as pd

# importing numpy
import numpy as np

data1 = [1,2,3,4,5]
data2 = [6,7,8,9,10]
data3 = [11,12,13,14,15,16,17,18,19,20]

# numpy array of length 7


# DataFrame with 2 columns of length 10
dataFrame1 = pd.DataFrame({'sepal_length(cm)': data1,
				'sepal_width(cm)': data2})
print("origonal frame is ")
print(dataFrame1)

dataFrame2 = pd.DataFrame({'width': data3})

newDataFrame = pd.concat([dataFrame1, dataFrame2], axis=1) 


print("new frame is")
print(newDataFrame)
