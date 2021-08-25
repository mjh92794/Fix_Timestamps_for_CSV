import pandas as pd
import csv

#Set the variables in Settings.csv before running the script
dataList = []
with open('Settings.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    for row in csv_reader:
        if line == 1:
            timeInterval = row[2]
            print("Time Interval = " + str(timeInterval))
            csvFileName = row[3]
            print("csvFileName = " + str(csvFileName))
        if line >= 1 and row[0] != '' and row[1] != '':
            dataList.append([row[0], row[1]])
        line += 1
print(dataList)

dfList = []
dataTypeList = []
df  = pd.read_csv(csvFileName + '.csv') #Import CSV
for n in dataList: #Run this for every data type (i.e. flow, depth, vel, rain, etc)
    dataTypeList.append(n[1]) #Make a list of the data types (flow, velocity, etc)
    df[n[0]] = pd.to_datetime(df[n[0]]) #Convert Time series data to the correct format
    dfList.append(df[[n[0], n[1]]].copy().set_index(n[0]).squeeze().dropna()) #Make a list of pandas data series, with empty data removed
mergedf = pd.concat(dfList, axis=1, keys=tuple(dataTypeList)).fillna('') #Align the time series between each data set and combine into one table with a single timeseries column
mergedf = mergedf.asfreq(timeInterval).copy() #You can comment out this line if you don't need even intervals
mergedf.to_csv(csvFileName + '_fixed.csv') #Export to CSV
